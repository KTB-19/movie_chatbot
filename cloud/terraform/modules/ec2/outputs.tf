output "instance_ids" {
  description = "The IDs of all the instances created"
  value       = aws_instance.instances[*].id
}