
# Azure Infra Notes

- Create Resource Group
- Create Azure Container Registry (ACR)
- Create two WebApps for Containers (Linux): API and Frontend
- Grant WebApps pull access to ACR (enable admin or use managed identity)
- Configure Frontend app setting: API_URL=https://<API_APP_NAME>.azurewebsites.net

CLI snippets:

az group create -n <RG> -l <REGION>
az acr create -n <REGISTRY_NAME> -g <RG> --sku Basic
az appservice plan create -n <PLAN> -g <RG> --is-linux --sku B1
az webapp create -n <API_APP_NAME> -g <RG> -p <PLAN> --deployment-container-image-name <REGISTRY_NAME>.azurecr.io/regression-api:latest
az webapp create -n <FRONTEND_APP_NAME> -g <RG> -p <PLAN> --deployment-container-image-name <REGISTRY_NAME>.azurecr.io/regression-frontend:latest
