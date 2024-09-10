output "crawling_ip" {
  value = module.crawling.instance_public_ip
}

output "backend_ip" {
  value = module.backend.instance_prviate_ip
}

