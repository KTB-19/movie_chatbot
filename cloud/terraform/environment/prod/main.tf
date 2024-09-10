####기본적인 terraform setup을 위한 tf 파일
# S3 버켓과 DynamoDB를 생성한다
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  backend "s3" {
    bucket               = "ktb-moviechabot-tfstate-bucket"
    key                  = "terraform.tfstate"
    region               = "ap-northeast-2"
    dynamodb_table       = "ktb-moviechatbot-tfstate-lock"
    encrypt              = true
    workspace_key_prefix = "workspaces"
  }
  required_version = ">= 1.2.0"
}


module "vpc" {
  source = "../../modules/vpc_v2"
}

module "security_groups" {
  source = "../../modules/security_groups"
  vpc_id = module.vpc.vpc_id
}

module "dev-host" {
  source          = "../../modules/ec2"
  subnets         = [module.vpc.public_subnets[0]]
  instance_type   = "t3.small"
  ami_image = "ami-05d768df76a2b8bd8"
  private_ips     = ["192.168.1.23"]
  instance_count  = 1
  security_groups = [module.security_groups.movie_default_sg_id]
  tags = "dev-host"
}

module "crawling" {
  source          = "../../modules/ec2"
  subnets         = [module.vpc.public_subnets[1]]
  instance_type   = "c6i.large"
  private_ips     = ["192.168.2.26"]
  instance_count  = 1
  security_groups = [module.security_groups.movie_default_sg_id]
  tags = "crawling"
}

module "backend" {
  source          = "../../modules/ec2"
  subnets         = module.vpc.private_subnets
  instance_type   = "t3.small"
  private_ips     = ["192.168.3.233", "192.168.4.134"]
  instance_count  = 2
  security_groups = [module.security_groups.movie_default_sg_id, module.security_groups.movie_backend_sg_id]
  tags = "backend"
}

module "db" {
  source          = "../../modules/ec2"
  subnets         = module.vpc.db_subnets
  instance_type   = "t3.micro"
  private_ips     = ["192.168.5.116"]
  instance_count  = 1
  security_groups = [module.security_groups.movie_default_sg_id, module.security_groups.movie_db_sg_id]
  tags = "db"
}

module "alb" {
  source = "../../modules/alb"
  target_instances_ids = module.backend.instance_ids
  vpc_id = module.vpc.vpc_id
  alb-subnets_ids = module.vpc.public_subnets
  security_groups_ids = [module.security_groups.movie_alb_sg_id]
}

# Front 배포 
resource "aws_s3_bucket" "react_website" {
  bucket = "ktb-movie-bucket-${terraform.workspace}"
}

# S3 버킷의 공용 접근 차단 설정
resource "aws_s3_bucket_public_access_block" "react_website_public_access_block" {
  bucket = aws_s3_bucket.react_website.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_cloudfront_origin_access_control" "s3_oac" {
  name                              = "ktb-movie-oac"
  description                       = "OAC for ktb-movie S3 bucket"
  origin_access_control_origin_type = "s3"

  signing_behavior = "always"
  signing_protocol = "sigv4"
}

resource "aws_cloudfront_distribution" "react_website_distribution" {
  origin {
    domain_name              = aws_s3_bucket.react_website.bucket_regional_domain_name
    origin_id                = aws_s3_bucket.react_website.id
    origin_access_control_id = aws_cloudfront_origin_access_control.s3_oac.id

  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = aws_s3_bucket.react_website.id

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    Name = "React Website Distribution"
  }
}

resource "aws_s3_bucket_policy" "react_website_policy" {
  bucket = aws_s3_bucket.react_website.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action = "s3:GetObject"
        Resource = "${aws_s3_bucket.react_website.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.react_website_distribution.arn
          }
        }
      }
    ]
  })
}