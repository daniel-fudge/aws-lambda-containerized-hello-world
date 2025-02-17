# AWS Lambda Containerized Hello World
Simple Hello World containerized Python 3.13 Lambda function.


## First set some environment variables
```shell
export AWS_ACCOUNT_ID=[ENTER AWS ACCOUNT ID HERE]
export AWS_PAGER=""
export BUCKET=[ENTER YOUR BUCKET NAME]
export IMAGE_NAME=hello-world
export IMAGE_TAG=v2
export LAMBDA_ROLE=lambda-execution
export REGION=us-east-1
```

## Commands to build image and verifiy that it was built
```shell
docker buildx build --platform linux/amd64 \
--provenance=false -t ${IMAGE_NAME}:$IMAGE_TAG .
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

## Create the Lambda function

### Create a Lambda execution role
You can create a role with the commandfs below or use an existing role.
```shell
aws iam create-role \
--role-name $LAMBDA_ROLE \
--assume-role-policy-document file://trust-policy.json
```
You need to attach the basic Lambda execution role.
```shell
aws iam attach-role-policy --role-name $LAMBDA_ROLE \
--policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name $LAMBDA_ROLE \
--policy-arn arn:aws:iam::aws:policy/service-role/AmazonS3FullAccess
```

### Create the actual Lambda function
```shell
aws lambda create-function \
--function-name $IMAGE_NAME --package-type Image \
--code ImageUri=$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/${IMAGE_NAME}:latest \
--role arn:aws:iam::${AWS_ACCOUNT_ID}:role/$LAMBDA_ROLE
```

### Change the timeout
```shell
aws lambda update-function-configuration --function-name $IMAGE_NAME --timeout 120
```

### Test the function
```shell
aws lambda invoke --function-name $IMAGE_NAME \
--payload '{"job_id": 1, "duration": 20}' --cli-binary-format raw-in-base64-out \
response.json
```

### Update the function
```shell
aws lambda update-function-code \
--function-name $IMAGE_NAME \
--image-uri $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/${IMAGE_NAME}:latest \
--publish
```


## References
https://docs.aws.amazon.com/lambda/latest/dg/images-create.html    
https://docs.aws.amazon.com/lambda/latest/dg/python-image.html    
https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/
