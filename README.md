# AWS Lambda Containerized Hello World
Simple Hello World containerized Python 3.8 Lambda function.

## Commands to build image and verifiy that it was built
```shell
docker build -t containerized-hello-world .
docker images containerized-hello-world
```

## References
https://docs.aws.amazon.com/lambda/latest/dg/images-create.html    
https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/
