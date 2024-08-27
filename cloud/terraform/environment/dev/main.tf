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
  source               = "../../modules/vpc"
  vpc_cidr             = "192.168.0.0/16"
  environment          = terraform.workspace
  public_subnet_count  = 2
  private_subnet_count = 1
}

## 인스턴스
module "backend" {
  source             = "../../modules/instance"
  ami_id             = "ami-0c2acfcb2ac4d02a0"
  instance_type      = "t3.small"
  ssh_key_name       = "kakao-tech-bootcamp"
  subnet_id          = module.vpc.private_subnet_ids[0]
  security_groups_id = [aws_security_group.ssh.id, aws_security_group.mysql.id]
  workspace          = "${terraform.workspace}-backend"
}

module "crawling" {
  source             = "../../modules/instance"
  ami_id             = "ami-0c2acfcb2ac4d02a0"
  instance_type      = "c6i.xlarge"
  ssh_key_name       = "kakao-tech-bootcamp"
  subnet_id          = module.vpc.public_subnet_ids[0]
  security_groups_id = [aws_security_group.ssh.id]
  workspace          = "${terraform.workspace}-crawling"
}

module "dev-host" {
  source             = "../../modules/instance"
  ami_id             = "ami-05d768df76a2b8bd8"
  instance_type      = "t3.small"
  ssh_key_name       = "kakao-tech-bootcamp"
  subnet_id          = module.vpc.public_subnet_ids[1]
  security_groups_id = [aws_security_group.ssh.id, aws_security_group.prometheus-host.id]
  workspace          = "Dev-Host"
}

# 보안 그룹
resource "aws_security_group" "ssh" {
  vpc_id = module.vpc.vpc_id
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9100
    to_port     = 9100
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "moive-${terraform.workspace}-sg-ssh"
  }
}

resource "aws_security_group" "mysql" {
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "moive-${terraform.workspace}-sg-mysql"
  }
}

resource "aws_security_group" "prometheus-host" {
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "moive-${terraform.workspace}-sg-prometheus-host"
  }
}

# // Cloud Front
# // S3 버킷생성
# resource "aws_s3_bucket" "movie_front_bucket" {
#   bucket = "ktb-${terraform.workspace}-front-bucket"
# }

# resource "aws_s3_bucket_website_configuration" "movie_bucket_web_config" {
#   bucket = aws_s3_bucket.movie_front_bucket.id
#   connection {
#     index
#   }
# }

# // Cloud Front
# resource "aws_cloudfront_origin_access_identity" "react_app_identity" {
#   comment = "Access identity for S3 bucket"
# }

# resource "aws_s3_bucket_policy" "movie_front_bucket_policy" {
#   bucket = aws_s3_bucket.movie_front_bucket.id

#   policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect = "Allow",
#         Principal = {
#           AWS = aws_cloudfront_origin_access_identity.react_app_identity.iam_arn
#         },
#         Action   = "s3:GetObject",
#         Resource = "${aws_s3_bucket.movie_front_bucket.arn}/*"
#       }
#     ]
#   })
# }

# resource "aws_cloudfront_distribution" "react_app_distribution" {
#   origin {
#     domain_name = aws_s3_bucket.movie_front_bucket.bucket_regional_domain_name
#     origin_id   = "S3-${aws_s3_bucket.movie_front_bucket.id}"

#     s3_origin_config {
#       origin_access_identity = aws_cloudfront_origin_access_identity.react_app_identity.cloudfront_access_identity_path
#     }
#   }

#   enabled             = true
#   is_ipv6_enabled     = true
#   comment             = "React app distribution"
#   default_root_object = "index.html"

#   default_cache_behavior {
#     allowed_methods  = ["GET", "HEAD"]
#     cached_methods   = ["GET", "HEAD"]
#     target_origin_id = "S3-${aws_s3_bucket.movie_front_bucket.id}"

#     forwarded_values {
#       query_string = false
#       cookies {
#         forward = "none"
#       }
#     }

#     viewer_protocol_policy = "redirect-to-https"
#     min_ttl                = 0
#     default_ttl            = 3600
#     max_ttl                = 86400
#   }

#   restrictions {
#     geo_restriction {
#       restriction_type = "none"
#     }
#   }

#   viewer_certificate {
#     cloudfront_default_certificate = true # CloudFront 기본 SSL 인증서를 사용하여 HTTPS 지원
#   }

#   depends_on = [ aws_s3_bucket.movie_front_bucket ]
# }

resource "aws_s3_bucket" "react_website" {
  bucket = "your-react-website-bucket"
  acl    = "private"

  block_public_acls   = true
  block_public_policy = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action    = "s3:GetObject"
        Resource  = "arn:aws:s3:::your-react-website-bucket/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = "arn:aws:cloudfront::<account-id>:distribution/<distribution-id>"
          }
        }
      }
    ]
  })
}