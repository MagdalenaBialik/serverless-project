resource "aws_lambda_function" "function" {
  function_name = "${var.app_name}-${var.function_suffix}"
  role          = var.lambda_role

  s3_bucket = var.s3_bucket_artifacts
  s3_key    = "${var.file_hash}.zip"

  handler = var.handler_name
  runtime = "python3.8"
  timeout = 30

  environment {
    variables = merge({
      dynamodb_table_name = var.dynamodb_table_name
    }, var.env_variables)

  }
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name = "/aws/lambda/${aws_lambda_function.function.function_name}"
}
