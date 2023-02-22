from flask import Flask, request, jsonify
from google.cloud import bigquery
import json

app = Flask(__name__)


# Define the route for the HTTP POST
@app.route('/insert_data', methods=['POST'])
def insert_data(request):
    # Get the JSON data from the request
    request_data = json.loads(request.data)
    # Get the name of the dataset to insert the data into
    dataset_name = "data_test_api"
    
    # Loop through each table in the JSON data
    for table_name, table_data in request_data["table"].items():
        # Get the data for the current table
        data = table_data["data"]
        # Get a reference to the table
        table_ref = client.dataset(dataset_name).table(table_name)
        table = client.get_table(table_ref)
        # Insert the data into the table
        errors = client.insert_rows(table, data)
        
        # Check if there were any errors
        if errors:
            return jsonify({"status": "error", "message": str(errors)})
    
    # If all data was inserted successfully, return a success message
    return jsonify({"status": "success"})
