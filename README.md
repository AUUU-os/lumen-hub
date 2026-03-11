# 🐺 LUMEN ORCHESTRATOR & HUB
**Status:** PROTO-ALPHA
**Location:** `E:\LUMEN_HUB`
**Operator:** SHAD

## 🏭 Philosophy
"Own the Code. Own the Runtime. Own the Metal."
LUMEN ORCHESTRATOR is a sovereign, local PaaS (Platform as a Service) that mimics the capabilities of Docker/Heroku/GitHub but runs natively on Windows via intelligent process isolation.

## 🏗️ Architecture

### 1. THE FORGE (`/repos`)
- **Role:** Source Code Management.
- **Tech:** Git (Bare Repositories).
- **Mechanism:** Users push code here. `post-receive` hooks trigger the Builder.

### 2. THE BUILDER (`/orchestrator/builder.py`)
- **Role:** CI/CD Pipeline.
- **Action:**
  1. Detects project type (Python/Node/Go).
  2. Creates isolated environment (`venv`, `node_modules`) in `/apps`.
  3. Installs dependencies (`pip install`, `npm install`).
  4. Generates a `Procfile` / startup script.

### 3. THE RUNNER (`/orchestrator/runner.py`)
- **Role:** Process Manager (Supervisor).
- **Action:**
  1. Spawns application processes.
  2. Assigns dynamic ports (starts from 9000).
  3. Monitors health (CPU/RAM).
  4. Auto-restarts on crash.

### 4. THE GATEWAY (`/orchestrator/gateway.py`)
- **Role:** Reverse Proxy & UI.
- **Tech:** FastAPI.
- **Action:** Routes `http://localhost/apps/my-app` to internal port `9001`.

## 📂 Directory Structure
- `repos/`: Git bare repositories (Push here).
- `apps/`: Deployed, running applications (Isolated envs).
- `data/`: Databases and persistent storage for apps.
- `orchestrator/`: The Engine code.

## 🚀 Usage Workflow
1. `lumen hub create my-api` -> Creates repo.
2. `git push lumen main` -> Triggers build.
3. System installs deps & starts app.
4. App available at `http://lumen.local/my-api`.

**AUUUUU!** 🐺💎
