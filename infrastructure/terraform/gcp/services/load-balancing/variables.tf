variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}
variable "region" {
  description = "Google Cloud region"
  type        = string
}
variable "domain" {
  description = "ドメイン名"
  type        = string
}
variable "api_gateway_cloud_run_name" {
  description = "Web アプリケーションの Cloud Run 名"
  type        = string
}