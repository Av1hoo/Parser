import polars as pl
from .base_parser import BaseParser

class TNSParser(BaseParser):
    def __init__(self, file_name, file_path):
        super().__init__(file_name, file_path)
        

    def detect(self):
        # Detect the appropriate parser based on file extension
        extension = self.file_name.filename.split('.')[-1].lower() 
        return extension in ['xlsx', 'xls']
        

    def parse(self):
        # The file is an excel file
        try:
            # Read the excel file, 2 blank rows at the top
            sheets = pl.read_excel(
                self.file_path,
                sheet_id=0,
                has_header=True,
                read_options={"header_row": 2},
            )

            # Check if multiple sheets are returned as a dict
            if isinstance(sheets, dict):
                # Extract the first sheet's DataFrame
                df = next(iter(sheets.values()))
            else:
                df = sheets  # It's already a DataFrame

            # First row is for labels
            df = df.rename({"<>":"Row"})

            # Split to formulations and controls
            formulations = df.columns[1:10]
            controls = df.columns[10:13]

            result = []
            for row in df.iter_rows(named=True):
                row_label = row["Row"] # A,B,C etc

                # get controls, no need to find every iteration
                control_values = [row[control] for control in controls]
                control_mean = sum(control_values) / len(control_values)

                #
                # Slice the 9 formulation columns in groups of 3 replicates each:
                #   Formulation #1 => columns [0:3] of formulation_cols
                #   Formulation #2 => columns [3:6]
                #   Formulation #3 => columns [6:9]
                #
                for i in range(0, 9, 3):
                    replicate_subset = formulations[i : i + 3]
                    replicate_values = [row[c] for c in replicate_subset]
                    replicate_values = [v for v in replicate_values if v is not None]

                    if not replicate_values:
                        continue  # skip if data is missing

                    formulation_mean = sum(replicate_values) / len(replicate_values)

                    # Figure out which "FORMULATION X" label applies
                    # We'll compute the number based on the row_label (A=0, B=1, etc.)
                    # plus i//3 to differentiate which set in that row
                    row_offset = ord(row_label.upper()) - ord("A")
                    # In each row we have 3 formulations, so each row contributes 3 IDs
                    # For example, row A => (0 * 3) + 1..3 => "FORMULATION 1..3"
                    # row B => (1 * 3) + 1..3 => "FORMULATION 4..6", etc.
                    formulation_number = row_offset * 3 + (i // 3 + 1)
                    formulation_id = f"FORMULATION {formulation_number}"

                    normalized_value = formulation_mean / control_mean
                    is_valid = normalized_value > 10

                    result.append({
                        "experiment_type": "TNS",
                        "row": row_label,
                        "formulation_id": formulation_id,
                        "calculated_value": normalized_value,
                        "is_valid": is_valid
                    })

            return result

        except Exception as e:
            raise Exception(f"Error parsing the file: {e}")