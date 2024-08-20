output "front_ip" {
  value = module.front.instance_public_ip
}

output "backend_ip" {
  value = module.backend.instance_prviate_ip
}

