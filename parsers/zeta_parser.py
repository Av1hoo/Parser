import polars as pl
from .base_parser import BaseParser

class ZetaParser(BaseParser):
    def __init__(self, file):
        super().__init__(file)

    def detect(self):
        # Detect the appropriate parser based on file extension
        extension = self.file.filename.split('.')[-1].lower() 
        return extension in ['csv']
        

    def parse(self):
        # The file is a csv file
        try:
            # Read the csv file
            df = pl.read_csv(self.file)

            # Rename the columns
            df = df.rename({
                "Sample Name": "SampleName",
                "Zeta Potential (mV)": "ZetaPotential"
            })

            # Split the data
            formulation_df = df.filter(pl.col("SampleName").str.starts_with("FORMULATION"))
            control_df = df.filter(pl.col("SampleName") == "STD 1")
            control_mean = control_df["ZetaPotential"].mean()

            # group by formulation id
            grouped = (
                            formulation_df
                            .groupby("SampleName", maintain_order=True)
                            .agg(pl.col("ZetaPotential").mean().alias("mean_reading"))
                        )
            
            results = []
            for row in grouped.iter_rows(named=True):
                formulation_id = row["SampleName"]
                mean_reading = row["mean_reading"]
                normalized = mean_reading / control_mean if control_mean != 0 else 0

                results.append({
                    "experiment_type": "Zeta Potential",
                    "formulation_id": formulation_id,
                    "calculated_value": normalized,
                    "is_valid": normalized > 0  # Valid if positive
                })

            return results            
                    
        except Exception as e:
            raise Exception(f"Error parsing the file: {e}")