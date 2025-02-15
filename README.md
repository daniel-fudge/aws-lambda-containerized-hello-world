# AWS Lambda Containerized Hello World
Simple Hello World containerized Python 3.13 Lambda function.

A video walk through can also be found [here](https://youtu.be/Pweawno2uw4) for the 
original Pytohn 3.9 version.

## First set some environment variables
```shell
export AWS_PAGER=""
export REGION=us-east-1
export IMAGE_NAME=hello-world
export IMAGE_TAG=v1
export AWS_ACCOUNT_ID=[ENTER AWS ACCOUNT ID HERE]
```

## Commands to build image and verifiy that it was built
```shell
docker buildx build --platform linux/amd64 --provenance=false -t ${IMAGE_NAME}:$IMAGE_TAG .
docker images 
```

#### Note
If trying to build mulitple times you may run out of disk space.   
`docker system df` will show the reclaimable disck space.   
`docker system prune -a` will delete all docker artifacts.   

## Pushing the image to ECR
### Configuring AWS CLI
To push the image to ECR from the CLI you need programmatic access and run `aws configure` 
or another access method.

### Authenticate Docker CLI with ECR
You should see `Login Succeeded` after this command.
```shell
aws ecr get-login-password --region $REGION | docker login --username AWS \
--password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
```

### Create an ECR repository
Note you only have to do this once. You may also simply use an existing repo.
```shell
aws ecr create-repository --repository-name $IMAGE_NAME --region $REGION \
--image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
```

### Give the image the `latest` tag
```shell
docker tag ${IMAGE_NAME}:${IMAGE_TAG} $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/${IMAGE_NAME}:latest
```

### Deploy Docker image to ECR
```shell 
docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/${IMAGE_NAME}:latest
```

## References
https://youtu.be/Pweawno2uw4   
https://docs.aws.amazon.com/lambda/latest/dg/images-create.html    
https://docs.aws.amazon.com/lambda/latest/dg/python-image.html    
https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/
