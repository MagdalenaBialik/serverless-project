output "lambda_function_name" {
  value = aws_lambda_function.pets-app-function.function_name
}

output "lambda_function_arn" {
  value = aws_lambda_function.pets-app-function.arn
}
