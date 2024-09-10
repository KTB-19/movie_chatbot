output "vpc_id" {
  value = aws_vpc.main_vpc.id
}

# Public 서브넷 ID 출력
output "public_subnets" {
  description = "Public subnet IDs"
  value = [
    for key, subnet in aws_subnet.subnets : subnet.id
    if substr(key, 0, 6) == "public"
  ]
}

# Private 서브넷 ID 출력
output "private_subnets" {
  description = "Private subnet IDs"
  value = [
    for key, subnet in aws_subnet.subnets : subnet.id
    if substr(key, 0, 7) == "private"
  ]
}

# DB 서브넷 ID 출력
output "db_subnets" {
  description = "DB subnet IDs"
  value = [
    for key, subnet in aws_subnet.subnets : subnet.id
    if substr(key, 0, 2) == "db"
  ]
}