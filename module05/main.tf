terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Variables
variable "resource_group_name" {
  description = "Name of existing resource group"
  type        = string
  default     = "dev-jhu-sa-rg-use01"
}

variable "acr_name" {
  description = "Name of existing Azure Container Registry"
  type        = string
  default     = "acrjhusa1"
}

variable "aks_name" {
  description = "Name for the AKS cluster"
  type        = string
  default     = "aks-jhu-sa-use01"
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.30"
}

variable "cpu_node_count" {
  description = "Number of nodes in CPU pool"
  type        = number
  default     = 2
}

variable "gpu_node_count" {
  description = "Number of nodes in GPU pool"
  type        = number
  default     = 1
}

variable "cpu_vm_size" {
  description = "VM size for CPU nodes"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "gpu_vm_size" {
  description = "VM size for GPU nodes"
  type        = string
  default     = "Standard_NC4as_T4_v3"  # Available in East US
}

# Reference existing resource group
data "azurerm_resource_group" "existing" {
  name = var.resource_group_name
}

# Reference existing ACR
data "azurerm_container_registry" "existing" {
  name                = var.acr_name
  resource_group_name = data.azurerm_resource_group.existing.name
}

# Create AKS Cluster with 2 Node Pools
resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.aks_name
  location            = data.azurerm_resource_group.existing.location
  resource_group_name = data.azurerm_resource_group.existing.name
  dns_prefix          = "aks-jhu-sa"
  # kubernetes_version will use the default supported version

  # Default/CPU Node Pool
  default_node_pool {
    name                = "cpupool"
    node_count          = var.cpu_node_count
    vm_size             = var.cpu_vm_size
    os_disk_size_gb     = 30
    type                = "VirtualMachineScaleSets"
    enable_auto_scaling = false
    
    # No taint on CPU pool - allows general workloads
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }

  tags = {
    Environment = "Dev"
    Project     = "AKS-GPU-Demo"
  }
}

# GPU Node Pool
resource "azurerm_kubernetes_cluster_node_pool" "gpu" {
  name                  = "gpupool"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  vm_size               = var.gpu_vm_size
  node_count            = var.gpu_node_count
  os_disk_size_gb       = 30
  enable_auto_scaling   = false
  
  # Taint to ensure only GPU workloads run here
  node_taints = ["sku=gpu:NoSchedule"]
  
  node_labels = {
    "workload" = "gpu"
  }

  tags = {
    Environment = "Dev"
    NodeType    = "GPU"
  }
}


# Outputs
output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "aks_cluster_id" {
  value = azurerm_kubernetes_cluster.aks.id
}

output "resource_group_name" {
  value = data.azurerm_resource_group.existing.name
}

output "acr_login_server" {
  value = data.azurerm_container_registry.existing.login_server
}

output "get_credentials_command" {
  value = "az aks get-credentials --resource-group ${data.azurerm_resource_group.existing.name} --name ${azurerm_kubernetes_cluster.aks.name}"
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}