from parsers.tns_parser import TNSParser
from parsers.zeta_parser import ZetaParser

def parse_file(file):
    # Detect the appropriate parser based on file extension
    tns_parser = TNSParser(file)
    zeta_parser = ZetaParser(file)

    if tns_parser.detect():
        return tns_parser.parse()
    elif zeta_parser.detect():
        return zeta_parser.parse()
    else:
        raise Exception("No parser found for the file")