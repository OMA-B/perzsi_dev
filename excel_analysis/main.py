from flask import Flask, request, jsonify,render_template, send_file
from flask_cors import CORS
from excel_analyzer import process_excel_file_for_analysis
import os


app = Flask('Excel Analyzer')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
CORS(app)
# db = SQLAlchemy(app)


#Home ROute
@app.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html')


# check urls for validation
@app.route('/excel_analyzer', methods=['POST'])
def url_checker():
	# retrieve the column name
	sheet_names = list(request.files.keys())[0]
	sheet_1_name = sheet_names.split(',')[0].strip()
	sheet_2_name = sheet_names.split(',')[1].strip()
	# retrieve the file and save the file name
	file = request.files[sheet_names]
	excel_filename = file.filename
	# Save the file to the server
	file.save(file.filename)

	response = process_excel_file_for_analysis(filename=file.filename, sheet_1_name=sheet_1_name, sheet_2_name= sheet_2_name)

	os.remove(path=file.filename)

	return jsonify({'message': response, 'filename': f'Analyzed_{excel_filename}'})

# for the checked urls file
@app.route('/excel_file')
def download_url_file():
    filename = 'output/analyzed_excel_result.xlsx'
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
	app.run()