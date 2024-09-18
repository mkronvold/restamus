from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

# Path to the CSV file
FILE_PATH = 'dhcp-reservation.csv'

# Read data from the CSV file
def read_file():
    data = {}
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 4:
                    mac, ipaddr, hostname, bootimage = row
                    data[mac] = {'ipaddr': ipaddr, 'hostname': hostname, 'bootimage': bootimage}
    return data

# Write data to the CSV file
def write_file(data):
    with open(FILE_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        for mac, values in data.items():
            writer.writerow([mac, values['ipaddr'], values['hostname'], values['bootimage']])

# Endpoint to get all data
@app.route('/data', methods=['GET'])
def get_data():
    data = read_file()
    return jsonify(data)

# Endpoint to get data by mac address
@app.route('/data/<mac>', methods=['GET'])
def get_data_by_mac(mac):
    data = read_file()
    if mac in data:
        return jsonify({mac: data[mac]})
    return jsonify({'error': 'MAC address not found'}), 404

# Endpoint to add or update data
@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.json
    if new_data:
        data = read_file()
        for mac, values in new_data.items():
            # if mac is in data, update values, else add new data only if all values are present
            if mac in data:
                data[mac].update(values)
            else:
                if 'ipaddr' in values and 'hostname' in values and 'bootimage' in values:
                    data[mac] = values
                else:
                    return jsonify({'error': 'All values are required for new mac'}), 400
        write_file(data)
        return jsonify({'message': 'Data added/updated successfully!'}), 201
    return jsonify({'error': 'No data provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
