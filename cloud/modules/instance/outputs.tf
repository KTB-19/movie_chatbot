output "instance_id" {
    value = aws_instance.ec2-instance.id
}

output "instance_public_ip" {
    value = aws_instance.ec2-instance.public_ip
}