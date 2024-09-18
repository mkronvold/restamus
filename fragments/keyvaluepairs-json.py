from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Path to the flat file
FILE_PATH = 'data.json'

# Read data from the flat file
def read_file():
    try:
        with open(FILE_PATH, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data

# Write data to the flat file
def write_file(data):
    with open(FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

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
