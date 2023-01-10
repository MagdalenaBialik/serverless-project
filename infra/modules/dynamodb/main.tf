resource "aws_dynamodb_table" "dynamodb_table" {
  name             = "${var.app_name}-statistics-table"
  read_capacity    = 5
  write_capacity   = 5
  hash_key         = "PK"
  range_key        = "SK"
  stream_enabled   = true
  stream_view_type = "NEW_IMAGE"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "N"
  }
}
