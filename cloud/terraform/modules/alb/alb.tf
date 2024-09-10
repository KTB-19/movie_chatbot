variable "alb-subnets_ids" {
  description = "alb에 등록할 subnet id"
  type = list(string)
}

variable "security_groups_ids" {
  type = list(string)
}

variable "vpc_id" {
  type = string
}

variable "target_instances_ids" {
  type = list(string)
}

# ALB 생성
resource "aws_lb" "backend_alb" {
  name               = "backend-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = var.security_groups_ids
  subnets            = var.alb-subnets_ids

  tags = {
    Name = "ktb-movie-backend-alb"
  }
}

resource "aws_lb_target_group" "backend_tg" {
  name        = "backend-tg"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = var.vpc_id

  health_check {
    path                = "/health"
    protocol            = "HTTP"
    matcher             = "200-299"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }
}

resource "aws_lb_listener" "backend_listener" {
  load_balancer_arn = aws_lb.backend_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend_tg.arn
  }
}

# 인스턴스 등록
resource "aws_lb_target_group_attachment" "backend" {
    count = length(var.target_instances_ids)
    target_group_arn = aws_lb_target_group.backend_tg.arn
    target_id        = var.target_instances_ids[count.index]
    port             = 8080
}