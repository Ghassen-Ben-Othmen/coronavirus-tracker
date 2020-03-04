import os
import json

def get_data():
    filename = os.path.join(os.getcwd(), 'data', 'data.json')
    with open(filename, 'r') as data:
        return json.load(data)