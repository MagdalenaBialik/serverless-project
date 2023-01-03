resource "aws_iam_role" "pet-role" {
  assume_role_policy = data.aws_iam_policy_document.iam_policy_document.json
  name               = "${var.app_name}-lambda-role"
}

resource "aws_iam_policy" "logging_policy" {
  name   = "${var.app_name}-logging-policy"
  policy = data.aws_iam_policy_document.function_logging_policy_document.json
}

resource "aws_iam_role_policy_attachment" "logging_policy_attachment" {
  role       = aws_iam_role.pet-role.id
  policy_arn = aws_iam_policy.logging_policy.arn
}

resource "aws_iam_policy" "dynamodb_policy" {
  name   = "${var.app_name}-dynamodb_policy"
  policy = data.aws_iam_policy_document.dynamodb_policy_document.json
}

resource "aws_iam_role_policy_attachment" "dynamodb_policy_attachment" {
  role       = aws_iam_role.pet-role.id
  policy_arn = aws_iam_policy.dynamodb_policy.arn
}
