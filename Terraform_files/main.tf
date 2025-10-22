resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_storage_account" "stg" {
  name                     = "driftteststorage01"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = var.account_tier
  account_replication_type = var.account_replication_type
  

}

resource "azurerm_storage_container" "container" {
  name                  = "driftcontainernew"                     # change as needed
  storage_account_name  = "driftteststorage01"                # your storage account name
  container_access_type = var.container_access_type                 # or "blob" / "container"
}
