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
  s3_bucket_artifacts = var.s3_bucket_artifacts
  env_variables       = { s3_bucket_name : module.photo-s3bucket.s3_bucket_name }
}

module "lambda_statistics" {
  source              = "./modules/lambda"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  lambda_role         = module.iam.iam_role_arn
  file_hash           = var.file_hash
  suffix              = "statistics"
  env_variables       = { s3_bucket_name : module.photo-s3bucket.s3_bucket_name }
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
  lambda_function_arn = module.lambda_statistics.lambda_function_arn
  function_name       = module.lambda_statistics.lambda_function_name
  cron_expression     = "cron(0 8 ? * 1 *)"
}

module "photo-s3bucket" {
  source   = "./modules/s3"
  app_name = var.app_name
}

module "ses" {
  source = "./modules/ses"
}
