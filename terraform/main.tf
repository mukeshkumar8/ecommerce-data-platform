terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "demo_bucket" {
  bucket = "ecommerce-terraform-demo-mukesh-2026"

  tags = {
    Name        = "Terraform Demo Bucket"
    Environment = "Learning"
    Project     = "Ecommerce Data Platform"
  }
}