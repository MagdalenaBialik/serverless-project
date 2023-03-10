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
  name   = "${var.app_name}-dynamodb-policy"
  policy = data.aws_iam_policy_document.dynamodb_policy_document.json
}

resource "aws_iam_role_policy_attachment" "dynamodb_policy_attachment" {
  role       = aws_iam_role.pet-role.id
  policy_arn = aws_iam_policy.dynamodb_policy.arn
}

resource "aws_iam_policy" "s3_policy" {
  name   = "${var.app_name}-s3-policy"
  policy = data.aws_iam_policy_document.allow_access_to_s3_policy_document.json
}

resource "aws_iam_role_policy_attachment" "s3_policy_attachment" {
  role       = aws_iam_role.pet-role.id
  policy_arn = aws_iam_policy.s3_policy.arn
}

resource "aws_iam_policy" "ses_policy" {
  name   = "${var.app_name}-ses-policy"
  policy = data.aws_iam_policy_document.ses_policy_document.json
}

resource "aws_iam_role_policy_attachment" "ses_policy_attachment" {
  role       = aws_iam_role.pet-role.id
  policy_arn = aws_iam_policy.ses_policy.arn
}
