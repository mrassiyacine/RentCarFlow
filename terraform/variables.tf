variable project_name {
  description = "The name of the GCP project"
  type        = string
}

variable "region" {
  description = "The region to deploy resources"
  type        = string
  default     = "europe-west1"
}

variable "zone" {
  description = "The zone to deploy resources"
  type        = string
  default     = "europe-west1-b"
}
