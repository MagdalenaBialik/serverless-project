resource "aws_ses_email_identity" "ses_identity" {
  email = "magdalena.bialik@gmail.com"
}

resource "aws_ses_domain_mail_from" "ses_from" {
  domain           = aws_ses_email_identity.ses_identity.email
  mail_from_domain = "magdalena.bialik@gmail.com"
}

resource "aws_ses_receipt_rule" "store" {
  name          = "store"
  rule_set_name = "default-rule-set"
  recipients = [
  "magdalena.bialik@gmail.com"]
  enabled      = true
  scan_enabled = true
  //
  //  lambda_action {
  //    function_arn = var.statistics_function_arn
  //    position     = 0
  //  }

}
