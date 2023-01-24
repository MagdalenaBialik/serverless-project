resource "aws_cloudwatch_event_rule" "lambda_event_rule" {
  name                = var.function_name
  schedule_expression = var.cron_expression
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  arn   = var.lambda_function_arn
  rule  = aws_cloudwatch_event_rule.lambda_event_rule.name
  input = jsonencode(var.lambda_input)
}

resource "aws_lambda_permission" "allow_cloudwatch_invoke_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = var.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_event_rule.arn
}
