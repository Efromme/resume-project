# 1. Existing Resume Site S3 Bucket
resource "aws_s3_bucket" "resume_bucket" {
  bucket        = var.domain_name
  force_destroy = false # ADDED: Matches live setting
  tags = {
    Name = "Resume Site Bucket"
  }
}

# Define the existing Origin Access Control (OAC)
resource "aws_cloudfront_origin_access_control" "resume_oac" {
  name                              = "ethanfromme.com-OAC"
  description                       = "-" # ADDED: Matches live setting
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
  origin_access_control_origin_type = "s3"
}

# 3. Existing CloudFront Distribution - ALL BLOCKS ARE NOW NESTED
resource "aws_cloudfront_distribution" "resume_cdn" {
  enabled = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  tags = {
    Name = "ethanfromme.com"
  }

  # CRITICAL: Add all your custom domain names here (Must be here AND in the cert)
  aliases = [var.domain_name] 
  
  # 1. ORIGIN BLOCK
  origin {
    connection_attempts      = 3
    connection_timeout       = 10
    # FIX: Use the complex S3 endpoint found in the plan
    domain_name              = "resume.ethanfromme.com.s3.us-east-1.amazonaws.com"
    origin_access_control_id = aws_cloudfront_origin_access_control.resume_oac.id
    # FIX: Use the complex ID found in the plan
    origin_id                = "resume.ethanfromme.com.s3.us-east-1.amazonaws.com-mf04xnmenj8" 
  }
  
   default_cache_behavior {
    # FIX: Use the specific cache policy ID instead of forwarded_values
    cache_policy_id        = "658327ea-f89d-4fab-a63d-7e88639e58f6"
    
    # FIX: Use the complex origin ID found in the plan
    target_origin_id       = "resume.ethanfromme.com.s3.us-east-1.amazonaws.com-mf04xnmenj8"
    viewer_protocol_policy = "redirect-to-https" 
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true
    
    # FIX: Remove the manual 'forwarded_values' block since 'cache_policy_id' is used
  }

  restrictions {
    geo_restriction {
      restriction_type = "none" 
    }
  }

  # 4. VIEWER CERTIFICATE BLOCK
  viewer_certificate {
    acm_certificate_arn      = "arn:aws:acm:us-east-1:158823976042:certificate/c54a45c4-9ca7-476e-af10-f533494a00b7"
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}