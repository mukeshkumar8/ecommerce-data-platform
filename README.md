# E-Commerce Data Platform

An end-to-end data engineering project using Python, PostgreSQL, and AWS.

## Project Overview

This project demonstrates an e-commerce data pipeline that processes CSV data, performs data cleaning and validation using Python, loads data into PostgreSQL, stores datasets in Amazon S3, and monitors the EC2 environment using Amazon CloudWatch.

## Architecture

CSV Data → Amazon S3 → EC2 → Python ETL → PostgreSQL → SQL Analytics

## Technologies

- Python
- Pandas
- PostgreSQL
- SQL
- Amazon S3
- Amazon EC2
- AWS IAM
- AWS Systems Manager Session Manager
- Amazon CloudWatch

## ETL Pipeline

1. Read cleaned CSV datasets
2. Validate and clean data using Python and Pandas
3. Load data into PostgreSQL
4. Perform data quality checks
5. Generate analytical reports
6. Monitor EC2 and ETL logs using CloudWatch

## Database Tables

- customers
- products
- orders
- order_items
- payments

## AWS Implementation

- Amazon S3 stores raw and cleaned datasets
- EC2 runs the Python ETL pipeline and PostgreSQL
- IAM provides least-privilege access to AWS services
- Systems Manager Session Manager provides secure EC2 access
- CloudWatch monitors CPU, memory, disk usage, and ETL logs

## Project Structure

ecommerce-data-platform/
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── reports/
├── src/
│   └── etl.py
├── requirements.txt
├── .gitignore
└── README.md

## Run the ETL

python src/etl.py

## Result

The project successfully demonstrates an end-to-end data engineering workflow from data ingestion and transformation to database loading, analytics, cloud storage, and monitoring.
# E-Commerce Data Platform

An end-to-end data engineering project using Python, PostgreSQL, and AWS.

## Project Overview

This project demonstrates an e-commerce data pipeline that processes CSV data, performs data cleaning and validation using Python, loads data into PostgreSQL, stores datasets in Amazon S3, and monitors the EC2 environment using Amazon CloudWatch.

## Architecture

CSV Data → Amazon S3 → EC2 → Python ETL → PostgreSQL → SQL Analytics

## Technologies

- Python
- Pandas
- PostgreSQL
- SQL
- Amazon S3
- Amazon EC2
- AWS IAM
- AWS Systems Manager Session Manager
- Amazon CloudWatch

## ETL Pipeline

1. Read cleaned CSV datasets
2. Validate and clean data using Python and Pandas
3. Load data into PostgreSQL
4. Perform data quality checks
5. Generate analytical reports
6. Monitor EC2 and ETL logs using CloudWatch

## Database Tables

- customers
- products
- orders
- order_items
- payments

## AWS Implementation

- Amazon S3 stores raw and cleaned datasets
- EC2 runs the Python ETL pipeline and PostgreSQL
- IAM provides least-privilege access to AWS services
- Systems Manager Session Manager provides secure EC2 access
- CloudWatch monitors CPU, memory, disk usage, and ETL logs

## Project Structure

ecommerce-data-platform/
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── reports/
├── src/
│   └── etl.py
├── requirements.txt
├── .gitignore
└── README.md

## Run the ETL

python src/etl.py

## Result

The project successfully demonstrates an end-to-end data engineering workflow from data ingestion and transformation to database loading, analytics, cloud storage, and monitoring.
