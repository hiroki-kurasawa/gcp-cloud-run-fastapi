locals {
  project = "adtech-sandbox"
  region = "asia-northeast1"
  zone = "asia-northeast1-a"
}

terraform {
  required_version = "~>0.14.0"
  backend "gcs" {
    bucket = "kurasawa_test"
    prefix = "terraform/sample-cloud-run"
  }
  required_providers {
    google = {
      version = "~>3.44"
    }
  }
}

provider "google" {
  project = local.project
  region = local.region
  zone = local.zone
}

resource "google_cloud_run_service" "kurasawa_test" {
  name = "kurasawatest"
  location = local.region
  template {
    spec {
      containers {
        image = "gcr.io/adtech-sandbox/kurasawatest:latest"
      }
    }
  }

  traffic {
    percent = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "member" {
  location = google_cloud_run_service.kurasawa_test.location
  project  = google_cloud_run_service.kurasawa_test.project
  service  = google_cloud_run_service.kurasawa_test.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
