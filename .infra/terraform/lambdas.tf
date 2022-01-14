module "lambda_streaming" {
  source            = "./modules/lambda"
  name              = "streaming"
  lambda_handler    = "stream.lambda_handler"
  dead_letter_queue = true
  memory_size       = 512
  cron              = { "expression" = "rate(5 minute)", "input" : { "wallet_address" = "0x8e3cfca4995d2ec53e1001707cd6f3d58a32b334", "stream_type" = "transaction" } }
  env               = { "bsc_scan_api_key" : local.bsc_scan_api_key }
}
