variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud region"
  type        = string
  default     = "asia-northeast1"
}

variable "domain" {
  description = "Cloud DNS で登録しているドメイン名"
  type        = string
}