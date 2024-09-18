from flask import Flask, request, jsonify

app = Flask(__name__)

# Path to the flat file
FILE_PATH = 'data.txt'

# Read data from the flat file
def read_file():
    with open(FILE_PATH, 'r') as file:
        data = file.read().splitlines()
    return data

# Write data to the flat file
def write_file(data):
    with open(FILE_PATH, 'w') as file:
        file.write('\n'.join(data))

# Endpoint to get data
@app.route('/data', methods=['GET'])
def get_data():
    data = read_file()
    return jsonify(data)

# Endpoint to add data
@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.json.get('data')
    if new_data:
        data = read_file()
        data.append(new_data)
        write_file(data)
        return jsonify({'message': 'Data added successfully!'}), 201
    return jsonify({'error': 'No data provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
