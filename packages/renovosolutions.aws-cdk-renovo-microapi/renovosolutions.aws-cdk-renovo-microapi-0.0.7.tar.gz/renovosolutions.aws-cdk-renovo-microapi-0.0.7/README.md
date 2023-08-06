# Renovo Solutions Private Lambda Micro REST API (`proxy`) Infrastructure Library

This infrastructure construct library implements a private lambda backed REST API on AWS API Gateway using `proxy+`. The basic concept is as follows:

* The API is made available on a private DNS address using a private DNS enabled VPC endpoint. Requests must route using the endpoint or they will not be allowed.
* The API has one method thats greedy and passes the request to Lambda
* This single method requires IAM auth
* The function runs and returns data back
* All API Gateway requests are logged to cloudwatch
* All lambda invokes are logged to cloudwatch
* Probably other things this readme currently forgot
