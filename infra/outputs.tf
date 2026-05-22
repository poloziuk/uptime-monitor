output "app_url" {
  value = "http://${aws_instance.app.public_ip}:8000"
}

output "public_ip" {
  value = aws_instance.app.public_ip
}

output "ssh_command" {
  value = var.enable_ssh ? "ssh -i <your-private-key> ubuntu@${aws_instance.app.public_ip}" : "SSH disabled — set enable_ssh=true to enable"
}
