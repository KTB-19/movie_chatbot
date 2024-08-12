variable "vpc_cidr" {
  description = "The CIDR block for the VPC"
  type        = string
}

variable "environment" {
  description = "The environment (e.g., dev, prod)"
  type        = string
}


variable "public_subnet_count" {
  description = "The number of public subnets"
  type        = number
}

variable "private_subnet_count" {
  description = "The number of private subnets"
  type        = number
}

variable "availability_zone" {
  description = "AZ"
  type = list(string)
  default = ["ap-northeast-2a"]
}