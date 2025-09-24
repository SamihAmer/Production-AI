terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Reference existing Resource Group 
data "azurerm_resource_group" "existing" {
  name = var.resource_group_name
}

# Create Azure Container Registry in existing resource group
resource "azurerm_container_registry" "main" {
  name                = var.acr_name
  resource_group_name = data.azurerm_resource_group.existing.name
  location           = data.azurerm_resource_group.existing.location
  sku                = var.acr_sku
  
  # Enable public network access 
  public_network_access_enabled = true
  
  # Enable admin user 
  admin_enabled = true

  tags = {
    Environment = "Development"
    Project     = "ACR-Demo"
  }
}