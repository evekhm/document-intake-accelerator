variable "views" {
  description = "View definitions."
  type = map(object({
    friendly_name       = string
    labels              = map(string)
    query               = string
    use_legacy_sql      = bool
    deletion_protection = bool
  }))
}

variable "project_id" {
  type        = string
  description = "project ID"
}