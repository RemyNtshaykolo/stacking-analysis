module "lambda_streaming" {
  source            = "./modules/lambda"
  name              = "streaming"
  lambda_handler    = "stream.lambda_handler"
  dead_letter_queue = true
  memory_size       = 256
  cron              = { "expression" : "rate(1 minute)" }
}
