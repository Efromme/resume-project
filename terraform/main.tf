terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  # CRITICAL: Remote State Backend
  # You MUST manually create the 'resume-ethanfromme-tf-state' bucket in AWS before step 2.
  backend "s3" {
    bucket         = "resume-ethanfromme-tf-state" # Must be globally unique!
    key            = "resume-project/terraform.tfstate"
    region         = "us-east-1"
    profile        = "default"
    encrypt        = true
    # dynamodb_table = "terraform-locks" # Recommended for team use
  }
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

# Used to get your AWS Account ID for ARNs during import/creation
data "aws_caller_identity" "current" {}