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

variable "project_id" {
  type        = string
  description = "specify the project name"
}

variable "vpc_network" {
  type        = string
  description = "specify the vpc name"
}

variable "subnetwork" {
  type = string
}

variable "serverless_subnet" {
  type = string
}

variable "region" {
  type        = string
  description = "GCP region"
}

variable "secondary_ranges_pods" {
  type = object({
    range_name    = string
    ip_cidr_range = string
  })
}

variable "secondary_ranges_services" {
  type = object({
    range_name    = string
    ip_cidr_range = string
  })
}

variable "source_subnetwork_ip_ranges_to_nat" {
  type        = string
  description = "Defaults to ALL_SUBNETWORKS_ALL_IP_RANGES. How NAT should be configured per Subnetwork. Valid values include: ALL_SUBNETWORKS_ALL_IP_RANGES, ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES, LIST_OF_SUBNETWORKS. Changing this forces a new NAT to be created."
  default     = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}

variable "master_cidr_ranges" {
  type        = list(any)
  description = "Master/Control Plan CIDR range to allow communication with GKE Node"
}

variable "node_pools_tags" {
  type        = list(any)
  description = "GKE Nodes tags to allow communication with Master/Control Plan"
}
