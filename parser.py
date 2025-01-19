# 1. Parse output files from various instruments (different parsing logic required)
# Automatically detect the appropriate parser based on file content.
# Support both CSV and Excel file formats.
# 2. Validate data based on provided business logic
# 3. Store valid results in an SQLite database
# 4. Provide a web interface for user interaction (is OK to skip CSS styling)
from flask import Flask, render_template, request, redirect, url_for

# web interface
app = Flask(__name__)

# load the files
files = []

# parse the files
def parse_files(files):
    pass

# validate the data
def validate_data(data):
    pass

# store the data
def store_data(data):
    pass

# show that data
def show_data():
    pass

if __name__ == '__main__':
    app.run(debug=True)