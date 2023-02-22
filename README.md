# Data Interaction with EndPoints developed using Cloud Function and BigQuery

This project contains the SQL queries required to create tables in BigQuery and import CSV data into those tables in Big Query. It also contains the Cloud Functions code to access to the EndPoints developed.

## Prerequisites

To follow these instructions, you will need:
- A Google Cloud Platform account
- Access to BigQuery, Google Cloud Storage and Google Cloud Functions
- Create a GCP Project
  -For this Example, we are using 'josito-api-data-gcp' project
## Setting Up BigQuery Tables

To create the tables in BigQuery, follow these steps:

1. Create a new dataset in BigQuery. In this case, we use 'data_test_api' as the dataset
2. Run the SQL queries in the `DDL_BQ_TABLES.sql` file to create the required tables.

## Import CSV to GCS (Google Cloud Storage)
To import CSV to GCS, follow these steps:

1. Create a new bucket. For this example, we use 'csv_historico' name
2. Upload the 3 CSV located in ./csv in this repository
3. Identify the URI of the 3 CSV in GCS


## Importing CSV Data

To import CSV data into the tables you created, follow these steps:

1. Ensure that the CSV files you want to import are stored in a Cloud Storage bucket.
2. Run the content of `/bd/DDL_BQ_TABLES.sql` in BigQuery
3. Run the `/bd/DML_BQ_FROM_CSV.sql` file to import the CSV data into the BigQuery tables created in the statement before.

## Setting Up Cloud Functions

To create the Cloud Functions that will serve as endpoints for your BigQuery tables, follow these steps:

1. Create a new Cloud Function for each endpoint in your Google Cloud Platform project (In this example we created 3 Cloud Functions).
2. Copy the contents of the `main.py` file for each function into the Cloud Function's source code editor.
4. Create a `requirements.txt` file for each function that lists the required dependencies. (Mainly Flask and BigQuery dependencies)
5. Deploy each Cloud Function.

## Using the Endpoints

Once your Cloud Functions are deployed, you can interact with your BigQuery table using the following endpoints:
Use this sintaxis for the endpoints: `https://[CLOUD_FUNCTION_REGION]-[PROJECT_ID].cloudfunctions.net/[FUNCTION_NAME]`

- `/rest_api_data_2_query1`: Retrieve the number of employees hired for each job and department in 2021 divided by quarter.
- `/rest_api_data_2_query2`: Retrieves the number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, grouped by department_id and department
-	`/rest_api_data`: Insert data passed through a JSON object you send in the request body. It can insert more than 1 row and insert rows to different tables

## Accessing the Endpoints

For this example, as a GET response, we have `rest_api_data_2_query1` and the `rest_api_data_2_query2` endpoints. So let's enter to those endpoints:

1. https://us-central1-josito-api-data-gcp.cloudfunctions.net/rest_api_data_2_query1
2. https://us-central1-josito-api-data-gcp.cloudfunctions.net/rest_api_data_2_query2

For POST request to insert data, we have `rest_api_data function`, so let's enter this command using curl to test it:

curl -m 510 -X POST https://us-central1-josito-api-data-gcp.cloudfunctions.net/rest_api_data -H "Authorization: bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -d '{
  "table": {
    "hired_employees_test": {
      "data": [
        {
			"id": 12300,
			"name": "Jose Taboada",
			"datetime": "2021-08-03T10:11:53Z",
			"department_id": 12,
			"job_id": 10
        },
        {
			"id": 12320,
			"name": "Alondra Urbe",
			"datetime": "2021-08-03T10:11:53Z",
			"department_id": 12,
			"job_id": 12
        }
      ]
    },
    "departments": {
      "data": [
        {
          "id": 50,
          "department": "Technology Consultancy"
        },
        {
          "id": 100,
          "department": "Data Engineering"
        }
      ]
    }
  }
}'
