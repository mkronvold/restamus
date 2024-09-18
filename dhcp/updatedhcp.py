#!/usr/bin/env python
import requests
import argparse

# Define the base URL of the REST API
BASE_URL = 'http://127.0.0.1:5000/data'

def update_data(mac, field, value):
    url = BASE_URL
    data = {
        mac: {
            field: value
        }
    }
    response = requests.post(url, json=data)
    try:
        response_json = response.json()
        if response.status_code == 201:
            print('Data updated successfully!')
        else:
            print(f'Failed to update data: {response_json}')
    except requests.exceptions.JSONDecodeError:
        print(f'Failed to update data: Non-JSON response received: {response.text}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update device information.')
    parser.add_argument('mac', type=str, help='MAC address of the device')
    parser.add_argument('field', type=str, choices=['ipaddr', 'hostname', 'boot'], help='Field to update')
    parser.add_argument('value', type=str, help='New value for the field')

    args = parser.parse_args()
    update_data(args.mac, args.field, args.value)
