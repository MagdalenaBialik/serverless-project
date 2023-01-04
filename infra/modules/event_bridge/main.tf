resource "aws_cloudwatch_event_rule" "add_pet_lambda_event_rule" {
  name                = "add-pet-lambda-rule"
  schedule_expression = "cron(0 8 ? * * *)"
}

resource "aws_cloudwatch_event_target" "add_pet_lambda_target" {
  arn  = var.lambda_function_arn
  rule = aws_cloudwatch_event_rule.add_pet_lambda_event_rule.name
}

resource "aws_lambda_permission" "allow_cloudwatch_to_add_pet_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = var.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.add_pet_lambda_event_rule.arn
}
