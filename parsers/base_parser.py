# parent class for all parsers
from abc import abstractmethod


class BaseParser:
    @abstractmethod
    def __init__(self, file):
        self.file = file

    @abstractmethod
    def detect(self):
        # Detect the appropriate parser based on file content
        pass
    
    @abstractmethod
    def parse(self):
        # Parse output files from various instruments - excel/csv
        pass