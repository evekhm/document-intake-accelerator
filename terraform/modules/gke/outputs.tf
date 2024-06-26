/**
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

output "gke_cluster" {
  value = try(module.gke_cluster.cluster_id, null)
}

output "endpoint" {
  value = try(module.gke_cluster.endpoint, null)
}

output "ca_certificate" {
  value = try(module.gke_cluster.ca_certificate, null)
}

output "service_account_email" {
 value = try(module.gke_cluster.service_account, null)
}