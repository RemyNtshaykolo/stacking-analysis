variable "name" {
  description = "Lambda name"
}

variable "lambda_handler" {
  description = "Path to lambda_handler function"
}

variable "reserved_concurrent_executions" {
  description = "Max concurrent executions"
  default     = -1
}

variable "memory_size" {
  description = "Max concurrent executions"
  default     = 128
}

variable "timeout" {
  description = "Lamda timeout in seconds"
  default     = 120
}

variable "image_uri" {
  description = "Docker image uri"
  default     = "408566731358.dkr.ecr.eu-west-3.amazonaws.com/crypto:lambda_image"
}

variable "dead_letter_queue" {
  description = "Add dead letter queue to lambda to retrieve event that failed"
  default     = false
  type        = bool
}

variable "cron" {
  description = "Add cron event with input"
  default     = null
  type        = any
}


variable "env" {
  description = "Env variables"
  type        = any
}



