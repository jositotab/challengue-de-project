--INSERCION DE DATOS A BQ
--HIRED_EMPLOYEES
LOAD DATA INTO josito-api-data-gcp.data_test_api.hired_employees_test
FROM FILES (
  format = 'CSV',
  uris = ['gs://csv_historico/hired_employees.csv'],
  max_bad_records = 100);
--DEPARTMENTS
LOAD DATA INTO josito-api-data-gcp.data_test_api.departments
FROM FILES (
  format = 'CSV',
  uris = ['gs://csv_historico/departamentos_test.csv']);
--JOBS
LOAD DATA INTO josito-api-data-gcp.data_test_api.jobs
FROM FILES (
  format = 'CSV',
  uris = ['gs://csv_historico/jobs.csv']);