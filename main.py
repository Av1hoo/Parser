import polars as pl
import os
import db
from parser import parse_file
from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)

# start the db
db.init_db()

# route to upload the file
UPLOAD_FOLDER = os.path.abspath('./uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET'])
def upload_form():
    return render_template('upload.html')

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return render_template("error.html", message="No file part in the request.")
    
    file = request.files["file"]
    if file.filename == "":
        return render_template("error.html", message="No file selected.")
    file_name = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
    file.save(file_path)

    # try to parse and validate the file
    try:
        results = parse_file(file_path)
        db.insert_results(results)
        # update the UI with the results
        return _render_parsed_results(results)
    except Exception as e:
        return render_template("error.html", message=str(e))
    
def _render_parsed_results(results):
    if not results:
        return render_template("error.html", message="No data found in the file.")
    
    df = pl.DataFrame(results)
    stats = {
        "Median": df["calculated_value"].median(),
        "Mean": df["calculated_value"].mean(),
        "STD": df["calculated_value"].std()
    }
    experiment_type = results[0]["experiment_type"]
    records = [
        {
            "formulation_id": result["formulation_id"],
            "calculated_value": result["calculated_value"],
            "is_valid": result["is_valid"]
        }
        for result in results
    ]

    return render_template("results.html", experiment_type=experiment_type, stats=stats, records=records)

@app.route('/experiments')
def experiments():
    experiment_types = db.fetch_experiment_types()
    return render_template('experiments.html', experiment_types=experiment_types)

@app.route('/results/<experiment_type>')
def view_results(experiment_type):
    rows = db.fetch_results(experiment_type)
    df = pl.DataFrame(
        {
            "formulation_id": [row[0] for row in rows],
            "calculated_value": [row[1] for row in rows],
            "is_valid": [row[2] for row in rows]
        }
    )
    
    # if empty
    if len(rows) == 0:
        return render_template("error.html", message="No data found for the experiment type.")
    
    stats = {
        "Median": df["calculated_value"].median(),
        "Mean": df["calculated_value"].mean(),
        "STD": df["calculated_value"].std()
    }

    records = df.to_dict(orient="records")
    return render_template("results.html", experiment_type=experiment_type, stats=stats, records=records)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
