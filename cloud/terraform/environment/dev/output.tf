output "crawling_ip" {
  value = module.crawling.instance_public_ip
}

output "db_ip" {
  value = module.db.instance_prviate_ip
}

output "front_ip" {
  value = module.front.instance_public_ip
}

output "backend_ip" {
  value = module.backend.instance_prviate_ip
}