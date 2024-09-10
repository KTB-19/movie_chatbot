resource "aws_instance" "instances" {
  count         = var.instance_count
  ami           = var.ami_image
  instance_type = var.instance_type
  subnet_id     = element(var.subnets, count.index)
  key_name = "kakao-tech-bootcamp"
  security_groups = var.security_groups
  private_ip    = var.private_ips[count.index]

  tags = {
    Name = "ktb-movie-${var.tags}-instance-${count.index}"
  }
}
