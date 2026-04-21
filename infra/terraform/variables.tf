variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "kubeconfig_path" {
  description = "Path to kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "resource-allocation-ai"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}
