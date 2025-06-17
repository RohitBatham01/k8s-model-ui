import streamlit as st
from kubernetes import client, config
from datetime import datetime


config.load_kube_config(config_file="/root/.kube/config")
v1 = client.CoreV1Api()

st.title("🤖 Kubernetes AI Model Deployer ")


model_images = {
    "gpt2": "tiangolo/uvicorn-gunicorn-fastapi:python3.9",  # demo container
    "bert": "shm007/bert-sentiment:latest",
    "nginx": "nginx"
}

default_ports = {
    "gpt2": 80,
    "bert": 5000,
    "nginx": 80
}

models = list(model_images.keys())
model = st.selectbox("Select AI Model", models)
cpu = st.text_input("CPU (e.g., 0.5, 1)", value="0.5")
memory = st.text_input("Memory (e.g., 512Mi, 1Gi)", value="1Gi")

pod_name = f"{model}-pod"
service_name = f"{model}-service"
container_port = default_ports[model]
node_port = 30080 + models.index(model)  

if st.button("Start Pod"):
    try:
        container = client.V1Container(
            name=pod_name,
            image=model_images[model],
            ports=[client.V1ContainerPort(container_port=container_port)],
            resources=client.V1ResourceRequirements(
                requests={"cpu": cpu, "memory": memory}
            )
        )
        pod = client.V1Pod(
            metadata=client.V1ObjectMeta(name=pod_name, labels={"app": model}),
            spec=client.V1PodSpec(containers=[container], restart_policy="Never")
        )
        v1.create_namespaced_pod(namespace="default", body=pod)

        
        service = client.V1Service(
            metadata=client.V1ObjectMeta(name=service_name),
            spec=client.V1ServiceSpec(
                type="NodePort",
                selector={"app": model},
                ports=[client.V1ServicePort(
                    port=container_port,
                    target_port=container_port,
                    node_port=node_port
                )]
            )
        )
        v1.create_namespaced_service(namespace="default", body=service)

        with open("pod_log.txt", "a") as log:
            log.write(f"[START] {pod_name} at {datetime.now()}\n")
        st.success(f"✅ Started: {pod_name} → http://13.233.116.126:{node_port}")
    except Exception as e:
        st.error(f"❌ Error starting pod: {e}")

if st.button("Stop Pod"):
    try:
        v1.delete_namespaced_pod(name=pod_name, namespace="default")
        v1.delete_namespaced_service(name=service_name, namespace="default")
        with open("pod_log.txt", "a") as log:
            log.write(f"[STOP] {pod_name} at {datetime.now()}\n")
        st.success(f"🛑 Stopped: {pod_name}")
    except Exception as e:
        st.error(f"❌ Error stopping pod: {e}")


st.subheader("📜 Pod Activity Log")
try:
    with open("pod_log.txt", "r") as log:
        st.text(log.read())
except FileNotFoundError:
    st.info("No logs yet.")

