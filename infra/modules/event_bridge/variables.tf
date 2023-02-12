variable "lambda_function_arn" {
  type = string
}

variable "function_name" {
  type = string
}

variable "cron_expression" {
  type = string
}

variable "lambda_input" {
  type    = map(any)
  default = {}
}

variable "event_name" {
  type = string
}
