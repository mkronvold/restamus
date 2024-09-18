from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

# Path to the CSV file
FILE_PATH = 'dddoc.csv'

# Read data from the CSV file
def read_file():
    data = {}
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 14:
                    docid, date, title, status, statement, context, decision, consequences, alternatives, jira, pr, refdocs, participants, notes = row
                    data[docid] = {'date': date, 'title': title, 'status': status, 'statement': statement, 'context': context, 'decision': decision, 'consequences': consequences, 'alternatives': alternatives, 'jira': jira, 'pr': pr, 'refdocs': refdocs, 'participants': participants, 'notes': notes}
    return data

# Write data to the CSV file
def write_file(data):
    with open(FILE_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        for docid, values in data.items():
            writer.writerow([docid, values['date'], values['title'], values['status'], values['statement'], values['context'], values['decision'], values['consequences'], values['alternatives'], values['jira'], values['pr'], values['refdocs'], values['participants'], values['notes']])

# Endpoint to get all data
@app.route('/data', methods=['GET'])
def get_data():
    data = read_file()
    return jsonify(data)

# Endpoint to get data by docid
@app.route('/data/<docid>', methods=['GET'])
def get_data_by_docid(docid):
    data = read_file()
    if docid in data:
        return jsonify({docid: data[docid]})
    return jsonify({'error': 'DOCID not found'}), 404

# Endpoint to add or update data
@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.json
    if new_data:
        data = read_file()
        for docid, values in new_data.items():
            # if docid is in data, update values, else add new data only if all values are present
            if docid in data:
                data[docid].update(values)
            else:
                if 'date' in values and 'title' in values and 'status' in values and 'statement' in values:
                    for key in 'context','decision','consequences','alternatives','jira','pr','refdocs','participants','notes':
                        if key not in values:
                            values[key] = ''
                    data[docid] = values
                else:
                    return jsonify({'error': 'Date, Title, Status and Statement values are required for new Docid'}), 400
        write_file(data)
        return jsonify({'message': 'Data added/updated successfully!'}), 201
    return jsonify({'error': 'No data provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
