variable "ami_id" {
    description = "ami image id for instance"
    type = string
}

variable "instance_type" {
    description = "ec2 instance type"
    type = string
    default = "t2.micro"
}

variable "ssh_key_name" {
    description = "Public key used to connect via ssh"
    type = string
    default = "kakao-tech-bootcamp"
}

variable "subnet_id" {
    description = "id for instance subnet"
    type = string
}

variable "security_groups_id" {
    description = "Security groups for instance"
    type = list(string)
}

variable "workspace" {
  description = "Current workspace name"
  type = string
}