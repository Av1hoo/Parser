# parent class for all parsers
from abc import abstractmethod


class BaseParser:
    @abstractmethod
    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path

    @abstractmethod
    def detect(self):
        # Detect the appropriate parser based on file content
        pass
    
    @abstractmethod
    def parse(self):
        # Parse output files from various instruments - excel/csv
        pass