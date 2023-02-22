--Big Query Table Creation (DDL)
CREATE TABLE `josito-api-data-gcp.data_test_api.hired_employees_test` 
(
id INT NOT NULL, name string NOT NULL, 
datetime string NOT NULL, 
department_id INT NOT NULL, 
job_id INT NOT NULL
);
CREATE TABLE `josito-api-data-gcp.data_test_api.departments` 
(
id INT  NOT NULL,
department string NOT NULL
);
CREATE TABLE `josito-api-data-gcp.data_test_api.jobs` 
(
id INT NOT NULL, 
job string NOT NULL
);