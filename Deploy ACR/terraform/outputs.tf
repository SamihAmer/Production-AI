output "acr_name" {
  description = "Name of the Azure Container Registry"
  value       = azurerm_container_registry.main.name
}

output "acr_login_server" {
  description = "Login server URL for the ACR"
  value       = azurerm_container_registry.main.login_server
}

output "resource_group_name" {
  description = "Name of the existing resource group"
  value       = data.azurerm_resource_group.existing.name
}

output "resource_group_location" {
  description = "Location of the existing resource group"
  value       = data.azurerm_resource_group.existing.location
}