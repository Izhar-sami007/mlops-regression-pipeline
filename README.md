
# MLOps Regression Pipeline (Scikit‑learn + FastAPI + Streamlit + Docker + Azure + GitHub Actions)

An end‑to‑end, production‑ready template for a **regression** ML use case using **Scikit‑learn** with:
- Training & evaluation
- Model serialization (`joblib`)
- FastAPI REST inference service
- Streamlit UI for interactive testing
- Dockerized services
- Azure Container Registry + App Service deployment
- CI/CD with GitHub Actions (build, test, push images, deploy)

---

## Quickstart

### 1) Create & activate env
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Train the model (produces `models/regressor.joblib`)
```bash
python training/train_model.py
```

### 3) Run locally (two terminals)

**API**
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Streamlit**
```bash
streamlit run frontend/app.py --server.port=8501
```

Open http://localhost:8501 and click **Predict**. (The UI calls the API at `http://localhost:8000/predict`.)

### 4) Docker (local)

Build images:
```bash
docker build -f Dockerfile.api -t mlops-reg-api:latest .
docker build -f Dockerfile.frontend -t mlops-reg-frontend:latest .
```

Run:
```bash
docker run -p 8000:8000 mlops-reg-api:latest
docker run -p 8501:8501 -e API_URL=http://host.docker.internal:8000 mlops-reg-frontend:latest
```

> On Linux, set `API_URL=http://172.17.0.1:8000` if needed.

---

## Azure Deployment (Containers)

**Prereqs**: Azure subscription, Azure CLI, Azure Container Registry (ACR), two Azure Web Apps for Containers (Linux) or a single multi-container WebApp with a compose file.

### 1) Push images to ACR
```bash
az acr login --name <REGISTRY_NAME>
docker tag mlops-reg-api:latest <REGISTRY_NAME>.azurecr.io/regression-api:latest
docker tag mlops-reg-frontend:latest <REGISTRY_NAME>.azurecr.io/regression-frontend:latest
docker push <REGISTRY_NAME>.azurecr.io/regression-api:latest
docker push <REGISTRY_NAME>.azurecr.io/regression-frontend:latest
```

### 2) Configure App Services
Point each Web App to its image in ACR (e.g. `regression-api:latest`, `regression-frontend:latest`).
Set **Application settings** on the frontend:
- `API_URL=https://<API_APP_NAME>.azurewebsites.net`

---

## CI/CD (GitHub Actions)

Add the following **Repository Secrets**:
- `AZURE_CREDENTIALS` — Service Principal JSON with access to RG + WebApps + ACR
- `ACR_LOGIN_SERVER` — e.g. `yourregistry.azurecr.io`
- `ACR_USERNAME` — ACR admin or SP username with push rights
- `ACR_PASSWORD` — password
- `RESOURCE_GROUP` — Azure resource group name
- `API_APP_NAME` — Azure Web App name for API
- `FRONTEND_APP_NAME` — Azure Web App name for Streamlit
- `REGISTRY_NAME` — ACR registry name (without domain)

The workflow:
- Lints & tests
- Builds Docker images
- Pushes to ACR with tag = commit SHA
- Updates Azure WebApps to the new image tags

---

## Project Structure

```
.
├── api/
│   └── main.py
├── frontend/
│   └── app.py
├── training/
│   └── train_model.py
├── models/                 # saved models (.joblib)
├── tests/
│   ├── test_api.py
│   └── test_training.py
├── Dockerfile.api
├── Dockerfile.frontend
├── requirements.txt
├── .github/workflows/ci-cd.yml
└── README.md
```

---

## Notes
- The training script uses **California Housing** dataset from scikit‑learn. Replace with your own data easily.
- For production, consider versioned models and a registry (e.g. MLflow) and add monitoring (Evidently/WhyLabs).

MIT License.
