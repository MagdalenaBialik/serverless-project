## Info
### Project
This AWS project is an serverless application that runs automatically using EventBridge events. 
### Daily flow:
Everyday a lambda function is triggered and chooses a random pet's name from a given list. The pets name and a timestamp are added to a DynamoDB Table. Using DynamoDB Streams another lambda is triggered and sends an email to an email list using AWS Simple Email Service (SES).
### Statistics
There are two lambdas that are using the data from DynamoDB Table to calculate pet's statistics.

##### Monthly

Monthly lambda calculates statistics on which pet has been chosen the most times overall and sends results once a month. There is also an S3 bucket that stores photos of every pet. A presigned URL to a photo of the pet who wins the statistics is sent alongside statistics in the email.
##### Weekly

Weekly lambda calculates statistics from last week and weekly sends an email with results. In this case photo from S3 is also send.

### Schema

This project is built using AWS Serverless Services according the schema shown below. Infrastucture was built using Terraform.



![Untitled Diagram drawio](https://user-images.githubusercontent.com/64687726/211026939-bdf5a6c5-6ad1-42e0-9e5c-2ea3df26dd5b.png)

