from flask import Flask, request, jsonify
from google.cloud import bigquery
import json

app = Flask(__name__)


@app.route('/hired_by_department_greater_that_mean', methods=['GET'])
def hired_by_department_greater_that_mean(request):
    try:
        bq_client = bigquery.Client(project="josito-api-data-gcp")
        query_job = bq_client.query("""
                    SELECT a.department_id, b.department, COUNT(*) AS num_hired_employees
                    FROM `josito-api-data-gcp.data_test_api.hired_employees_test` a
                    JOIN `josito-api-data-gcp.data_test_api.departments` b
                      ON a.department_id = b.id
                    WHERE EXTRACT(YEAR FROM PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', datetime)) = 2021
                    GROUP BY department_id, b.department
                    HAVING COUNT(*) > (SELECT AVG(num_employees) AS mean_num_employees
                      FROM (
                        SELECT COUNT(*) AS num_employees
                        FROM `josito-api-data-gcp.data_test_api.hired_employees_test`
                        WHERE EXTRACT(YEAR FROM PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', datetime)) = 2021
                        GROUP BY department_id))
                    ORDER BY COUNT(*) DESC;
        """)
        results = query_job.result()

        # Create a list of dictionaries to represent the results
        data = []
        for row in results:
            data.append({
                'department_id': row.department_id,
                'department': row.department,
                'num_hired_employees': row.num_hired_employees
            })

        return jsonify({'data': data})

    except Exception as e:
        return f"An error occurred: {str(e)}", 500