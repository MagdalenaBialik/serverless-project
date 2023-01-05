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

module "lambda_add_pet" {
  source              = "./modules/lambda"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  lambda_role         = module.iam.iam_role_arn
  file_hash           = var.file_hash
  suffix              = var.add_pet_function_suffix
  s3_bucket_name      = module.photo-s3bucket.s3_bucket_name
}

module "lambda_statistics" {
  source              = "./modules/lambda"
  app_name            = var.app_name
  dynamodb_table_name = module.dynamodb.dynamodb_table_name
  lambda_role         = module.iam.iam_role_arn
  file_hash           = var.file_hash
  suffix              = var.statistic_function_suffix
  s3_bucket_name      = module.photo-s3bucket.s3_bucket_name

}

module "event_bridge" {
  source              = "./modules/event_bridge"
  lambda_function_arn = module.lambda_add_pet.lambda_function_arn
  function_name       = module.lambda_add_pet.lambda_function_name
  cron_expression     = "cron(0 8 ? * * *)"
}

module "photo-s3bucket" {
  source   = "./modules/s3"
  app_name = var.app_name
}
