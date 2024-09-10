# Output for movie-default security group
output "movie_default_sg_id" {
  description = "The ID of the movie-default security group"
  value       = aws_security_group.movie-default.id
}

# Output for movie-db security group
output "movie_db_sg_id" {
  description = "The ID of the movie-db security group"
  value       = aws_security_group.movie-db.id
}

# Output for movie-alb security group
output "movie_alb_sg_id" {
  description = "The ID of the movie-alb security group"
  value       = aws_security_group.movie-alb.id
}

# Output for movie-backend security group
output "movie_backend_sg_id" {
  description = "The ID of the movie-backend security group"
  value       = aws_security_group.movie-backend.id
}