terraform {
  cloud {
    organization = "bialik-magdalena"

    workspaces {
      name = "serverless-project"
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.33.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}

module "dynamodb" {
  source   = "./modules/dynamodb"
  app_name = var.app_name
}

module "iam" {
  source              = "./modules/iam"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  s3_bucket_name      = module.photo-s3bucket.s3_bucket_name
  ses_identity        = module.ses.ses_identity_arn
}

module "lambda_add_pet" {
  source              = "./modules/lambda"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  lambda_role         = module.iam.iam_role_arn
  file_hash           = var.file_hash
  suffix              = "add_pet"
  function_suffix     = "add_pet"
  s3_bucket_artifacts = var.s3_bucket_artifacts
  env_variables = {
    s3_bucket_name : module.photo-s3bucket.s3_bucket_name,
  }
}

resource "aws_lambda_event_source_mapping" "this" {
  event_source_arn  = module.dynamodb.dynamodb_table_arn
  function_name     = module.lambda_dynamodb_stream.lambda_function_arn
  starting_position = "LATEST"
}

module "lambda_dynamodb_stream" {
  source              = "./modules/lambda"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  lambda_role         = module.iam.iam_role_arn
  file_hash           = var.file_hash
  suffix              = "dynamodb_stream"
  function_suffix     = "dynamodb_stream"
  s3_bucket_artifacts = var.s3_bucket_artifacts
  env_variables = {
    s3_bucket_name : module.photo-s3bucket.s3_bucket_name,
    email_title = "Pet of the day",
  }
}


module "lambda_statistics_weekly" {
  source              = "./modules/lambda"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  lambda_role         = module.iam.iam_role_arn
  file_hash           = var.file_hash
  suffix              = "statistics"
  function_suffix     = "weekly_statistics"
  env_variables = {
    s3_bucket_name : module.photo-s3bucket.s3_bucket_name,
    days        = 7,
    email_title = "Pet of the days weekly statistics"
  }
  s3_bucket_artifacts = var.s3_bucket_artifacts
}

module "lambda_statistics_overall" {
  source              = "./modules/lambda"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  lambda_role         = module.iam.iam_role_arn
  file_hash           = var.file_hash
  suffix              = "statistics"
  function_suffix     = "overall_statistics"
  env_variables = {
    s3_bucket_name : module.photo-s3bucket.s3_bucket_name,
    email_title = "Pet of the days overall statistics"
  }
  s3_bucket_artifacts = var.s3_bucket_artifacts
}

module "event_bridge_add_pet" {
  source              = "./modules/event_bridge"
  lambda_function_arn = module.lambda_add_pet.lambda_function_arn
  function_name       = module.lambda_add_pet.lambda_function_name
  cron_expression     = "cron(0 8 ? * * *)"
}

module "event_bridge_weekly_statistics" {
  source              = "./modules/event_bridge"
  lambda_function_arn = module.lambda_statistics_weekly.lambda_function_arn
  function_name       = module.lambda_statistics_weekly.lambda_function_name
  cron_expression     = "cron(0 8 ? * 1 *)"
}

module "event_bridge_monthly_statistics" {
  source              = "./modules/event_bridge"
  lambda_function_arn = module.lambda_statistics_overall.lambda_function_arn
  function_name       = module.lambda_statistics_overall.lambda_function_name
  cron_expression     = "cron(0 8 1 * ? *)"
}

module "photo-s3bucket" {
  source   = "./modules/s3"
  app_name = var.app_name
}

module "ses" {
  source = "./modules/ses"
}
