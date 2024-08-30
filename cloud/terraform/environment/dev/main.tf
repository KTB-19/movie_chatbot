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
  security_groups_id = [aws_security_group.ssh.id, aws_security_group.backend.id]
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

# ALB

# ALB를 위한 보안 그룹 생성
resource "aws_security_group" "alb" {
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
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
    Name = "moive-${terraform.workspace}-sg-alb"
  }
}

# ALB 생성
resource "aws_lb" "alb" {
  name               = "${terraform.workspace}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnet_ids

  tags = {
    Name = "moive-${terraform.workspace}-alb"
  }
}

# ALB 리스너 생성
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend.arn
  }
}

# 타겟 그룹 생성
resource "aws_lb_target_group" "backend" {
  name     = "${terraform.workspace}-tg-backend"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id

  health_check {
    path                = "/"
    protocol            = "HTTP"
    matcher             = "200-299"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }

  tags = {
    Name = "moive-${terraform.workspace}-tg-backend"
  }
}

# 백엔드 인스턴스 등록
resource "aws_lb_target_group_attachment" "backend" {
  target_group_arn = aws_lb_target_group.backend.arn
  target_id        = module.backend.instance_id
  port             = 8080
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

resource "aws_security_group" "backend" {
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  #mysql
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  #alb
  ingress {
    from_port       = 80
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
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