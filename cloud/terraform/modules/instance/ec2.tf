resource "aws_instance" "ec2-instance" {
    ami = var.ami_id
    instance_type = var.instance_type
    key_name = var.ssh_key_name
    subnet_id = var.subnet_id
    security_groups = var.security_groups_id

    tags = {
        Name = "movie-${var.workspace}-instance"
    }
}

