variable "resource_group_name" {
  description = "Name of the existing resource group"
  type        = string
  default     = "dev-jhu-sa-rg-use01"
}

variable "acr_name" {
  description = "Name of the Azure Container Registry"
  type        = string
  default     = "acrjhusa1"  
}

variable "acr_sku" {
  description = "SKU for the ACR"
  type        = string
  default     = "Basic"
}