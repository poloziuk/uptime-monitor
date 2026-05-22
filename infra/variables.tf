variable "aws_region" {
  default = "us-east-1"
}

variable "instance_type" {
  default = "t3.micro"
}

variable "image_tag" {
  description = "Docker image tag to pull from GHCR (injected by CI as git SHA)"
  default     = "latest"
}

variable "enable_ssh" {
  description = "Open port 22 and attach a key pair — flip to true when debugging"
  type        = bool
  default     = false
}

variable "ssh_public_key" {
  description = "SSH public key content. Only used when enable_ssh = true."
  default     = ""
}
