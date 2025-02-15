# AWS Lambda Containerized Hello World
Simple Hello World containerized Python 3.13 Lambda function.

A video walk through can also be found [here](https://youtu.be/Pweawno2uw4) for the 
original Pytohn 3.9 version.
## Commands to build image and verifiy that it was built
```shell
docker build -t containerized-hello-world .
docker images containerized-hello-world
```

#### Note
If trying to build mulitple times you may run out of disk space.   
`docker system df` will show the reclaimable disck space.   
`docker system prune -a` will delete all docker artifacts.   
If you run out of memory, you may need to enlarge the Cloud9 instance.


## References
https://youtu.be/Pweawno2uw4   
https://docs.aws.amazon.com/lambda/latest/dg/images-create.html    
https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/
