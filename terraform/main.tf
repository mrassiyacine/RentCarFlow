terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.17.0"
    }
  }
  backend "gcs" {
    bucket  = "terraform-state-bucket"
    prefix  = "terraform/state"

  }
}

provider "google" {
  project = var.project_name
  region  = var.region
  zone    = var.zone
}
