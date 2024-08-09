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
  public_subnet_cidr   = "192.168.1.0/24"
  private_subnet_cidr  = "192.168.2.0/24"
  environment          = terraform.workspace
  public_subnet_count  = 2
  private_subnet_count = 2
}

module "ec2" {
  source             = "../../modules/instance"
  ami_id             = "ami-0c2acfcb2ac4d02a0"
  instance_type      = "t2.micro"
  ssh_key_name       = "Bryan"
  subnet_id          = module.vpc.public_subnet_ids[0]
  security_groups_id = [aws_security_group.ssh.id]
  workspace          = "${terraform.workspace}-crawling"
}

module "db" {
  source             = "../../modules/instance"
  ami_id             = "ami-0c2acfcb2ac4d02a0"
  instance_type      = "t2.small"
  ssh_key_name       = "Bryan"
  subnet_id          = module.vpc.private_subnet_ids[0]
  security_groups_id = [aws_security_group.mysql.id]
  workspace          = "${terraform.workspace}-db"
}

resource "aws_security_group" "ssh" {
  vpc_id = module.vpc.vpc_id
  ingress {
    from_port   = 22
    to_port     = 22
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

output "crawling" {
  value = module.ec2.instance_public_ip
}

output "db" {
  value = module.db.instance_public_ip
}