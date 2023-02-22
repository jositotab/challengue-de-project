from flask import Flask, request, jsonify, render_template
from google.cloud import bigquery
import json
import os

app = Flask(__name__)

@app.route('/get_hiring_metrics_per_quarter', methods=['GET'])
def get_hiring_metrics_per_quarter(request):
    try:
        # Initialize BigQuery client
        bq_client = bigquery.Client(project="josito-api-data-gcp")
        # Execute query
        query_job = bq_client.query("""
                    SELECT b.department, c.job, 
                      COUNT(CASE 
                              WHEN EXTRACT(QUARTER FROM PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', datetime)) = 1 THEN 1 
                              ELSE NULL 
                            END) AS Q1,
                      COUNT(CASE 
                              WHEN EXTRACT(QUARTER FROM PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', datetime)) = 2 THEN 1 
                              ELSE NULL 
                            END) AS Q2,
                      COUNT(CASE 
                              WHEN EXTRACT(QUARTER FROM PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', datetime)) = 3 THEN 1 
                              ELSE NULL 
                            END) AS Q3,
                      COUNT(CASE 
                              WHEN EXTRACT(QUARTER FROM PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', datetime)) = 4 THEN 1 
                              ELSE NULL 
                            END) AS Q4
                    FROM `josito-api-data-gcp.data_test_api.hired_employees_test`
                    JOIN `josito-api-data-gcp.data_test_api.departments` b ON department_id = b.id
                    JOIN `josito-api-data-gcp.data_test_api.jobs` c ON job_id = c.id
                    WHERE EXTRACT(YEAR FROM PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', datetime)) = 2021
                    GROUP BY department, job
                    ORDER BY department, job
        """)
        results = query_job.result()
        # Process query results
        data = []
        for row in results:
            data.append({
                'department': row.department,
                'job': row.job,
                'q1': row.Q1,
                'q2': row.Q2,
                'q3': row.Q3,
                'q4': row.Q4
            })
        
        return jsonify({'data': data})
        #return render_template('table.html', data=data, template_folder='./')

    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    