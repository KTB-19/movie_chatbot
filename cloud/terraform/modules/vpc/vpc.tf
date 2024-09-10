resource "aws_vpc" "this" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "movie-chat-${var.environment}-vpc"
  }
}

resource "aws_subnet" "public" {
  count = var.public_subnet_count

  vpc_id            = aws_vpc.this.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  map_public_ip_on_launch = true
  availability_zone = var.availability_zone[count.index]

  tags = {
    Name = "movie-chat-${var.environment}-public-subnet-${count.index + 1}"
  }
}

resource "aws_subnet" "private" {
  count = var.private_subnet_count

  vpc_id            = aws_vpc.this.id
  cidr_block        = cidrsubnet(var.vpc_cidr,   8, var.public_subnet_count + count.index)
  availability_zone = var.availability_zone[count.index % length(var.availability_zone)]

  tags = {
    Name = "movie-chat-${var.environment}-private-subnet-${count.index + 1}"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "movie-chat-${var.environment}-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "movie-chat-${var.environment}-public-rt"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.this.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.movie-nat-gw.id
  }

  tags = {
    Name = "movie-chat-${var.environment}-private-rt"
  } 
}

resource "aws_route_table_association" "public" {
  count = var.public_subnet_count

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count = var.private_subnet_count

  subnet_id = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

resource "aws_eip" "movie-eip" {
  vpc = true
}

# Nat Gateway
resource "aws_nat_gateway" "movie-nat-gw" {
  allocation_id = aws_eip.movie-eip.id
  subnet_id = aws_subnet.public[0].id
  connectivity_type = "public"
}