#!/bin/bash
set -e

. ./scripts/set_env.sh

aws --region ${AWS_REGION} ecr get-login-password | docker login --password-stdin --username AWS ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
docker build -f "Dockerfile.LambdaImage" -t ${TF_VAR_lambda_image} --secret id=aws,src=$HOME/.aws/credentials .
docker push "${TF_VAR_lambda_image}"
