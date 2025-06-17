# 🚀 Kubernetes AI Model Deployer

This project provides a minimal UI to deploy and manage AI models on Kubernetes using user-defined CPU and memory configurations.

---

## ✅ Features

- Select from 5 AI models
- Enter CPU and memory limits
- Start and stop Kubernetes pods
- View log history of pod actions

---

## 🧰 Stack

- UI: Streamlit
- Backend: Python with subprocess & kubectl
- Kubernetes: K3s (running on AWS EC2 Free Tier)
- Logging: Plaintext (`pod_log.txt`)

---

## 🛠️ How to Set Up (AWS EC2 + K3s)

### 1. 🖥️ Launch AWS EC2
- OS: Amazon Linux 2023 
- Instance type: `t3.medium` 
- Open ports: 22, 3000 ,443

### 2. ⚙️ Install K3s
```bash
curl -sfL https://get.k3s.io | sh -
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# k8s-model-ui
# k8s-model-ui
