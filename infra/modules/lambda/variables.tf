variable "app_name" {
  type = string
}

variable "lambda_role" {
  type = string
}

variable "dynamodb_table_name" {
  type = string
}

variable "file_hash" {
  type = string
}

variable "handler" {
  type = string
}

variable "function_suffix" {
  type = string
}

variable "s3_bucket_artifacts" {
  type = string
}

variable "env_variables" {
  type    = map(any)
  default = {}
}
