from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

# Path to the CSV file
FILE_PATH = 'generic.csv'

# Read data from the CSV file
def read_file():
    data = {}
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 14:
                    index, column_a, column_b, column_c, column_d, column_e, column_f, column_g, column_h, column_i, column_j, column_k, column_l, column_m = row
                    data[index] = {'column_a': column_a, 'column_b': column_b, 'column_c': column_c, 'column_d': column_d, 'column_e': column_e, 'column_f': column_f, 'column_g': column_g, 'column_h': column_h, 'column_i': column_i, 'column_j': column_j, 'column_k': column_k, 'column_l': column_l, 'column_m': column_m}
    return data

# Write data to the CSV file
def write_file(data):
    with open(FILE_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        for index, values in data.items():
            writer.writerow([index, values['column_a'], values['column_b'], values['column_c'], values['column_d'], values['column_e'], values['column_f'], values['column_g'], values['column_h'], values['column_i'], values['column_j'], values['column_k'], values['column_l'], values['column_m']])

# Endpoint to get all data
@app.route('/data', methods=['GET'])
def get_data():
    data = read_file()
    return jsonify(data)

# Endpoint to get data by index
@app.route('/data/<index>', methods=['GET'])
def get_data_by_index(index):
    data = read_file()
    if index in data:
        return jsonify({index: data[index]})
    return jsonify({'error': 'index not found'}), 404

# Endpoint to add or update data
@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.json
    if new_data:
        data = read_file()
        for index, values in new_data.items():
            # if index is in data, update values, else add new data only if all values are present
            if index in data:
                data[index].update(values)
            else:
                if 'column_a' in values and 'column_b' in values and 'column_c' in values and 'column_d' in values:
                    for key in 'column_e','column_f','column_g','column_h','column_i','column_j','column_k','column_l','column_m':
                        if key not in values:
                            values[key] = ''
                    data[index] = values
                else:
                    return jsonify({'error': 'column_a, column_b, column_c and column_d values are required for new index'}), 400
        write_file(data)
        return jsonify({'message': 'Data added/updated successfully!'}), 201
    return jsonify({'error': 'No data provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
