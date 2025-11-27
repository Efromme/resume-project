variable "aws_region" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "aws_profile" {
  description = "The AWS profile used for local execution."
  type        = string
  default     = "default"
}

variable "domain_name" {
  description = "The root domain name for the resume site."
  type        = string
  default     = "resume.ethanfromme.com"
}