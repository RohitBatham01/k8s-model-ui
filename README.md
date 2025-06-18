# 🤖 Kubernetes AI Model Deployer

A full-stack Streamlit UI that lets users deploy and manage AI model pods (like GPT-2, BERT) on a single-node Kubernetes (K3s) cluster hosted on an AWS EC2 instance.

---

## 📦 Features

- ✅ Deploy models: GPT2, BERT, GPTJ, LLaMA (placeholder), NGINX
- ✅ Input CPU & Memory limits before deployment
- ✅ One-click pod deployment from browser UI
- ✅ Kubernetes Pod + NodePort Service created automatically
- ✅ Stop pods and clean services from the UI
- ✅ Activity logs recorded and displayed live

---

## 🧠 How It Works (Explanation)

### 🎯 Goal

The goal is to allow users to deploy lightweight AI models from a browser without using `kubectl`.

### ⚙️ Components

| Component         | Role                                                      |
|------------------|-----------------------------------------------------------|
| **Streamlit UI** | Web frontend to trigger model deployment                  |
| **Python Backend** | Uses Kubernetes SDK to interact with K3s                 |
| **Docker**        | Containers the UI for portability                         |
| **Docker Compose** | Simplifies launching the app                             |
| **K3s Kubernetes** | Deploys pods and services                                |
| **AWS EC2**       | Host for everything (OS, Docker, K3s, App, Models)        |

### 🔁 Flow

1. User selects model (e.g., `bert`) and sets CPU/memory in the UI.
2. Python backend:
   - Creates Kubernetes Pod using model's Docker image.
   - Exposes it via NodePort (e.g., `30081`).
3. App logs `[START]` and `[STOP]` events to `pod_log.txt`.
4. Models become accessible via `http://<EC2-IP>:30081`.
5. Users can stop pods with one click — services are deleted too.

---

## 🏗️ Architecture

Browser (Port 3000)
↓
Streamlit UI (Docker)
↓
Kubernetes Python SDK
↓
K3s (Installed on EC2)
↓
[Pod + NodePort Service]


---

## ⚙️ Tech Stack

| Layer            | Tool/Service                                  |
|------------------|-----------------------------------------------|
| Infrastructure   | AWS EC2 (t3.medium, Amazon Linux 2023)        |
| K8s              | K3s (Lightweight single-node Kubernetes)      |
| UI Framework     | Streamlit                                     |
| Containerization | Docker + Docker Compose                       |
| AI Model Images  | `nginx`, `shm007/bert-sentiment`, etc.        |
| K8s Interface    | Kubernetes Python SDK                         |

---

## 🚀 Setup Instructions

### 1. Launch EC2

- AMI: Amazon Linux 2023
- Type: `t3.medium`
- Open ports: `22`, `3000`, `30080–30084`

### 2. SSH & Install K3s

```bash
ssh -i your-key.pem ec2-user@<EC2-IP>
curl -sfL https://get.k3s.io | sh -
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
mkdir -p /root/.kube
cp /etc/rancher/k3s/k3s.yaml /root/.kube/config

