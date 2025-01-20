import polars as pl
from .base_parser import BaseParser

class TNSParser(BaseParser):
    def __init__(self, file):
        super().__init__(file)

    def detect(self):
        # Detect the appropriate parser based on file extension
        extension = self.file.filename.split('.')[-1].lower() 
        return extension in ['xlsx', 'xls']
        

    def parse(self):
        # The file is an excel file
        try:
            # Read the excel file, 2 blank rows at the top
            df = pl.read_excel(self.file, header=2)

            # First row is for labels
            df = df.rename({"<>":"Row"})

            # Split to formulations and controls
            formulations = df.columns[1:9]
            controls = df.columns[9:13]

            result = []
            for row in df.iter_rows(named=True):
                row_label = row["Row"] # A,B,C etc

                # get controls, no need to find every iteration
                control_values = [row[control] for control in controls]
                control_mean = sum(control_values) / len(control_values)

                for i, formula in enumerate(formulations, start=1):
                    formulation_id = f"FORMULATION {((ord(row_label) - ord('A')) * 3) + i}" 

                    # get three and find mean
                    formultion_values = [row[formulation] for formulation in formulations[i-1:i+2]]
                    formultion_mean = sum(formultion_values) / len(formultion_values)

                    # normalize
                    normalized_value = formultion_mean / control_mean if control_mean != 0 else 0

                    result.append({
                        "experiment_type": "TNS",
                        "row": row_label,
                        "formulation_id": formulation_id,
                        "calculated_value": normalized_value,
                        "is_valid": normalized_value > 10
                    })

            return result
                    

        except Exception as e:
            raise Exception(f"Error parsing the file: {e}")