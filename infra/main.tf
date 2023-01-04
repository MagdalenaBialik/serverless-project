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
}

module "lambda" {
  source              = "./modules/lambda"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  lambda_role         = module.iam.iam_role_arn
  file_hash           = var.file_hash
}

module "event_bridge" {
  source              = "./modules/event_bridge"
  lambda_function_arn = module.lambda.lambda_function_arn
  function_name       = module.lambda.lambda_function_name
  cron_every_day      = "cron(0 8 ? * * *)"
}
