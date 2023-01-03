data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "iam_policy_document" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]
    effect = "Allow"
    sid    = ""
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }
  }
}

data "aws_iam_policy_document" "dynamodb_policy_document" {
  statement {
    actions = [
      "dynamodb:GetItem",
      "dynamodb:Query",

    ]
    resources = ["arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/${var.dynamodb_table_name}"]

    effect = "Allow"
  }
}

data "aws_iam_policy_document" "function_logging_policy_document" {
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:*:*"]

    effect = "Allow"
  }
}
