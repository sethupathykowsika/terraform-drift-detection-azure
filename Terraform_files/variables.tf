variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
}

variable "location" {
  description = "Azure Region"
  type        = string
}

variable "account_tier" {
  description = "The tier of the storage account"
  type        = string
  
}

variable "account_replication_type" {
  description = "The replication type of the storage account"
  type        = string
  
}

variable "container_access_type" {
  type = string
}