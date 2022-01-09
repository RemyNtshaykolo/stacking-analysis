resource "aws_iam_role" "lambda" {
  name               = var.name
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "lambda" {
  function_name = var.name
  role          = aws_iam_role.lambda.arn
  image_config {
    command = [var.lambda_handler]
  }
  package_type                   = "Image"
  image_uri                      = var.image_uri
  timeout                        = var.timeout
  memory_size                    = var.memory_size
  reserved_concurrent_executions = var.reserved_concurrent_executions

  #   environment {
  #     variables = {
  #       foo = "bar"
  #     }
  #   }
}

resource "aws_iam_role_policy_attachment" "cloudwatch" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_sqs_queue" "lambda_dead_letter_queue" {
  count = var.dead_letter_queue ? 1 : 0
  name  = "${var.name}-dead-letter-queue"
}

resource "aws_cloudwatch_event_rule" "cron" {
  count               = local.cron ? 1 : 0
  schedule_expression = var.cron["expression"]
}

resource "aws_cloudwatch_event_target" "cron" {
  count = local.cron ? 1 : 0
  rule  = aws_cloudwatch_event_rule.cron[0].name
  arn   = aws_lambda_function.lambda.arn
  input_transformer {
    input_paths = { "time" = "$.time" }

    input_template = <<INPUT_TEMPLATE_EOF
    {
        "timestamp":<time>
    }
    INPUT_TEMPLATE_EOF
  }
}

resource "aws_lambda_permission" "cron" {
  count         = local.cron ? 1 : 0
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.cron[0].arn
}
