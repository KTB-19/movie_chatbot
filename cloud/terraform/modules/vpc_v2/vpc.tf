
# 공통 태그 정의
locals {
  common_tags = {
    Project     = "ktb-movie"
    Owner       = "Cloud-Team-Bryan"
    CreatedBy   = "Terraform"
    CreatedDate = formatdate("YYYY-MM-DD", timestamp())
  }

  # 서브넷 정의
  subnets = {
    public = {
      cidr_blocks = ["192.168.1.0/24", "192.168.2.0/24"]
      azs         = ["ap-northeast-2a", "ap-northeast-2c"]
    }
    private = {
      cidr_blocks = ["192.168.3.0/24", "192.168.4.0/24"]
      azs         = ["ap-northeast-2a", "ap-northeast-2c"]
    }
    db = {
      cidr_blocks = ["192.168.5.0/24"]
      azs         = ["ap-northeast-2a"]
    }
  }

    subnet_config = {
        public  = local.subnets.public
        private = local.subnets.private
        db      = local.subnets.db
    }

  subnet_map = merge([
    for subnet_type, config in local.subnet_config : {
      for idx, cidr in config.cidr_blocks :
      "${subnet_type}-${idx}" => {
        cidr_block        = cidr
        availability_zone = config.azs[idx]
        public            = subnet_type == "public"
      }
    }
  ]...)
}

# VPC 생성
resource "aws_vpc" "main_vpc" {
  cidr_block           = "192.168.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(local.common_tags, {
    Name = "ktb-movie-main-vpc"
  })
}

# 인터넷 게이트웨이
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id

  tags = merge(local.common_tags, {
    Name = "ktb-movie-main-igw"
  })
}

resource "aws_subnet" "subnets" {
  for_each = local.subnet_map

  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = each.value.cidr_block
  availability_zone       = each.value.availability_zone
  map_public_ip_on_launch = each.value.public

  tags = merge(local.common_tags, {
    Name = "ktb-movie-${each.key}-subnet"
  })
}

# NAT Gateway
resource "aws_eip" "nat_eip" {
  vpc = true
  tags = merge(local.common_tags, {
    Name = "ktb-movie-nat-eip"
  })
}

resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.subnets["public-0"].id

  tags = merge(local.common_tags, {
    Name = "ktb-movie-nat-gateway"
  })
}

# 라우팅 테이블
resource "aws_route_table" "route_tables" {
  for_each = toset(["public", "private"])

  vpc_id = aws_vpc.main_vpc.id

  tags = merge(local.common_tags, {
    Name = "ktb-movie-${each.key}-route-table"
  })
}

# 라우팅 규칙
resource "aws_route" "public_internet_gateway" {
  route_table_id         = aws_route_table.route_tables["public"].id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_route" "private_nat_gateway" {
  route_table_id         = aws_route_table.route_tables["private"].id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat_gateway.id
}

# 서브넷 연결
resource "aws_route_table_association" "subnet_routes" {
  for_each = aws_subnet.subnets

  subnet_id      = each.value.id
  route_table_id = aws_route_table.route_tables[startswith(each.key, "public") ? "public" : "private"].id
}