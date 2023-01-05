resource "aws_lambda_function" "function" {
  function_name = "${var.app_name}-${var.suffix}"
  role          = var.lambda_role

  s3_bucket = "pets-app-artifacts"
  s3_key    = "${var.file_hash}.zip"

  handler = "app.${var.suffix}.handler"
  runtime = "python3.8"

  environment {
    variables = {
      dynamodb_table_name = var.dynamodb_table_name
      s3_bucket_name      = var.s3_bucket_name
    }
  }
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name = "/aws/lambda/${aws_lambda_function.function.function_name}"
}
