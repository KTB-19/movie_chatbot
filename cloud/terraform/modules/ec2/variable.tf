variable "subnets" {
  description = "서브넷 주소"
  type = list(string)
  nullable = true
}
variable "tags" {
  type = string
}

variable "instance_count" {
  description = "생성할 인스턴스 개수"
  type = number
}

variable "instance_type" {
  description = "인스턴스 타입"
  type = string
  default = "t2.micro"
}

variable "security_groups" {
  description = "Security Groups"
  type = list(string)
}

variable "private_ips" {
  description = "할당한 private subnet"
  type = list(string)
}

variable "ami_image" {
  description = "EC2 이미지"
  type = string
  default = "ami-0c2acfcb2ac4d02a0"
}