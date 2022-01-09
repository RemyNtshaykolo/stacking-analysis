data "aws_secretsmanager_secret" "secrets" {
  arn = "arn:aws:secretsmanager:eu-west-3:408566731358:secret:secrets-bMNRm3"
}

data "aws_secretsmanager_secret_version" "secrets" {
  secret_id = data.aws_secretsmanager_secret.secrets.id
}
