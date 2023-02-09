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
  //  ses_identity        = module.ses.ses_identity_arn
}

module "lambda_add_pet" {
  source              = "./modules/lambda"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  lambda_role         = module.iam.iam_role_arn
  file_hash           = var.file_hash
  handler_name        = "handlers.add_pet.handler"
  function_suffix     = "add_pet"
  s3_bucket_artifacts = var.s3_bucket_artifacts
  env_variables = {
    s3_bucket_name : module.photo-s3bucket.s3_bucket_name,
  }
}

module "lambda_dynamodb_stream" {
  source              = "./modules/lambda"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  lambda_role         = module.iam.iam_role_arn
  file_hash           = var.file_hash
  handler_name        = "handlers.mail_pet_stream.handler"
  function_suffix     = "dynamodb_stream"
  s3_bucket_artifacts = var.s3_bucket_artifacts
  env_variables = {
    s3_bucket_name : module.photo-s3bucket.s3_bucket_name,
    email_title = "Pet of the day",
  }
}

resource "aws_lambda_event_source_mapping" "this" {
  event_source_arn  = module.dynamodb.dynamodb_table_stream_arn
  function_name     = module.lambda_dynamodb_stream.lambda_function_arn
  starting_position = "LATEST"
}


module "lambda_statistics" {
  source              = "./modules/lambda"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  lambda_role         = module.iam.iam_role_arn
  file_hash           = var.file_hash
  handler_name        = "handlers.mail_statistics.handler"
  function_suffix     = "statistics"
  env_variables = {
    s3_bucket_name : module.photo-s3bucket.s3_bucket_name
  }
  s3_bucket_artifacts = var.s3_bucket_artifacts
}


module "event_bridge_add_pet" {
  event_name          = "pets_app_add_pet"
  source              = "./modules/event_bridge"
  lambda_function_arn = module.lambda_add_pet.lambda_function_arn
  function_name       = module.lambda_add_pet.lambda_function_name
  cron_expression     = "cron(0 8 ? * * *)"
}

module "event_bridge_weekly_statistics" {
  event_name          = "pets_app_weekly_stat"
  source              = "./modules/event_bridge"
  lambda_function_arn = module.lambda_statistics.lambda_function_arn
  function_name       = module.lambda_statistics.lambda_function_name
  cron_expression     = "cron(0 8 ? * 1 *)"
  lambda_input        = { days : 7, email_title = "Pet of the days weekly statistics" }
}

module "event_bridge_monthly_statistics" {
  event_name          = "pets_app_overall_stat"
  source              = "./modules/event_bridge"
  lambda_function_arn = module.lambda_statistics.lambda_function_arn
  function_name       = module.lambda_statistics.lambda_function_name
  cron_expression     = "cron(0 8 ? * * *)"
  lambda_input        = { days : null, email_title = "Pet of the days overall statistics" }
}

module "photo-s3bucket" {
  source   = "./modules/s3"
  app_name = var.app_name
}

//module "ses" {
//  source = "./modules/ses"
//}
