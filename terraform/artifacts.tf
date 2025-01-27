resource "google_artifact_registry_repository" "my-repo" {
  location      = var.region
  repository_id = "docker-images"
  description   = "containerized services with cleanup policies"
  format        = "DOCKER"
  cleanup_policy_dry_run = false
  cleanup_policies {
    id     = "delete-untagged"
    action = "DELETE"
    condition {
      tag_state    = "UNTAGGED"
    }
  }
}
