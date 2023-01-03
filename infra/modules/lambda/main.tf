resource "aws_lambda_function" "pets-app-function" {
  function_name = "${var.app_name}-lambda-add-pet"
  role          = var.lambda_role
  filename      = "${path.module}/appka.zip"
  handler       = "main.handler"
  runtime       = "python3.8"

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = var.dynamodb_table_name
    }
  }
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name = "/aws/lambda/${aws_lambda_function.pets-app-function.function_name}"
}