# StoriCard send emails
Exercise related to the analysis and calculus of balance by month

## About the Project
This project is a solution in AWS Lambda, who is triggered anytime that a file is updated to a bucket S3, the process read the file, persist the information in a DynamoDB, and finally get all the information and then made the necessary calculation for get the balance, debit and credit

## Prerequisites

Create a table in DynamoDb, with the following structure:
Table:transactions-stori
Model:Id, Date, Transaction, all string fields

Create a Bucket in S3 called "transactions-gvm", where is going to be persisted the csv file

Create a trigger from the bucket to the main lambda, who is the responsible of execute the process

## Usage

Create the lambda to connect to the database using an http crud transaction
After that please configure the api gateway creating an endpoint and using the integrations of the previous lambda 


## License
[MIT](https://choosealicense.com/licenses/mit/)
