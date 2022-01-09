#!/bin/bash
# read -p 'Select environment: ' stage

app_name=$(cat package.json | jq -r .name)

export AWS_PROFILE=remy_nts_ci_cd
export AWS_ACCOUNT_ID=408566731358
export TF_VAR_app_name=${app_name} 
export TF_WORKSPACE=${stage}
export AWS_REGION="eu-west-3"
export TF_VAR_lambda_image=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${TF_VAR_app_name}:lambda_image