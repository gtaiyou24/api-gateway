terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.34.0"
    }
  }
}
# GCPプロバイダー の設定
provider "google" {
  project = var.project_id
  region  = var.region
}

module "apis" {
  source = "../../services/apis"
  project_id = var.project_id
  enable_apis = [
    "artifactregistry.googleapis.com",  # Artifact Registry
    "run.googleapis.com",               # Cloud Run
    "compute.googleapis.com",           # Compute Engine
    "iam.googleapis.com",               # IAM
    "iamcredentials.googleapis.com",    # IAM
  ]
  wait_for_seconds = 180
}

module "api_gateway" {
  source = "../../services/api-gateway"
  project_id = var.project_id
  region = var.region

  depends_on = [module.apis]
}

module "load_balancing" {
  source = "../../services/load-balancing"
  project_id = var.project_id
  region = var.region
  domain = var.domain
  api_gateway_cloud_run_name = module.api_gateway.name

  depends_on = [module.api_gateway]
}
