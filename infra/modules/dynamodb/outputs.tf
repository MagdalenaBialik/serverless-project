output "dynamodb_table_name" {
  value = aws_dynamodb_table.dynamodb_table.name
}

output "dynamodb_table_stream_arn" {
  value = aws_dynamodb_table.dynamodb_table.stream_arn
}
