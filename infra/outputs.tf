output "lambda_function" {
  description = "Lambda function"
  value       = module.lambda_add_pet.lambda_function_name
}
