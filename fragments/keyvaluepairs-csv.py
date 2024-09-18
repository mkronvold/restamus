from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

# Path to the CSV file
FILE_PATH = 'data.csv'

# Read data from the CSV file
def read_file():
    data = {}
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    key, value = row
                    data[key] = value
    return data

# Write data to the CSV file
def write_file(data):
    with open(FILE_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        for key, value in data.items():
            writer.writerow([key, value])

# Endpoint to get all data
@app.route('/data', methods=['GET'])
def get_data():
    data = read_file()
    return jsonify(data)

# Endpoint to get data by key
@app.route('/data/<key>', methods=['GET'])
def get_data_by_key(key):
    data = read_file()
    if key in data:
        return jsonify({key: data[key]})
    return jsonify({'error': 'Key not found'}), 404

# Endpoint to add or update data
@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.json
    if new_data:
        data = read_file()
        data.update(new_data)
        write_file(data)
        return jsonify({'message': 'Data added/updated successfully!'}), 201
    return jsonify({'error': 'No data provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
