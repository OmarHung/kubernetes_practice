# 安裝
## Download the latest release:
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
```

## Validate the binary (optional):
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | shasum -a 256 --check
```

If valid, the output is:
```
kubectl: OK
```
If the check fails, shasum exits with nonzero status and prints output similar to:

```
kubectl: FAILED
shasum: WARNING: 1 computed checksum did NOT match
```

## Make the kubectl binary executable.

```bash
chmod +x ./kubectl
```
Move the kubectl binary to a file location on your system PATH.

```bash
sudo mv ./kubectl /usr/local/bin/kubectl
sudo chown root: /usr/local/bin/kubectl
```

## Test to ensure the version you installed is up-to-date:

```bash
kubectl version --client
```

## After installing and validating kubectl, delete the checksum file:

```bash
rm kubectl.sha256
```
# Minikube：能夠在PC上的虛擬機運行單一節點(single-node) Kubernetes cluster 的工具。
## Install Minikube
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube
```

# Kubernetes 基礎運行
確認皆安裝完畢後，開啟命令列即可開始第一次的測試

## 啟動 Minikube 和建立 cluster
```bash
minikube start
```
現在，你可以利用 kubectl 與你的 cluster 互動了。讓我們利用現存的 image echoserver 建立一個 Kubernetes Deployment，它是一個簡單的 HTTP 伺服器以及利用 --port 將8080埠公開。
```bash
kubectl create deployment hello-minikub --image=k8s.gcr.io/echoserver:1.10
```
為了要能夠存取 hello-minikube Deployment，將它公開為一項 Service
```bash
kubectl expose deployment hello-minikub --type=NodePort --port=8080
```
選項 --type=NodePort 規定 Service 的類型
hello-minikube Pod 現在已經啟動了，但你必須在利用公開的 Service 存取它之前等待該 Pod 上線。
確認 Pod 是否上線並運行：
```bash
kubectl get pod
```
如果輸出顯示 STATUS 為 ContainerCreating，則 Pod 正在建立中；如果輸出顯示 STATUS 為 Running，則表示該 Pod 正在線上並運行。
取得公開的 Service 的 URL 檢視 Service 詳細資料：
```bash
minikube service hello-minikub --url
```
為了查看本地的 cluster 的詳細資料，複製並貼上你從輸出畫面得到的 URL 在瀏覽器上。
輸出應該像這樣：
```
Hostname: hello-minikube-7c77b68cff-8wdzq

Pod Information:
    -no pod information available-

Server values:
    server_version=nginx: 1.13.3 - lua: 10008

Request Information:
    client_address=172.17.0.1
    method=GET
    real path=/
    query=
    request_version=1.1
    request_scheme=http
    request_uri=http://192.168.99.100:8080/

Request Headers:
    accept=*/*
    host=192.168.99.100:30674
    user-agent=curl/7.47.0

Request Body:
    -no body in request-
```
如果你不想 Service 和 cluster 繼續運行，你可以刪除它們。
刪除 hello-minikube Service:
```bash
kubectl delete services hello-minikub
```
刪除 hello-minikube Deployment
```bash
kubectl delete deployment hello-minikub
```
停止本地 Minikube cluster:
```bash
minikube stop
```
刪除本地 Minikube cluster
```bash
minikube delete
```

# FastAPI Deployment 和 Service：
## fastapi-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
        - name: fastapi
          image: fastapi-app:latest
          ports:
            - containerPort: 8000
          env:
            - name: MONGO_URL
              value: "mongodb://mongo:27017"
            - name: REDIS_URL
              value: "redis://redis:6379"
```

## 部署到 Minikube
```bash
kubectl apply -f fastapi-deployment.yaml
```
## 注意事項：
- Service 類型：使用 ClusterIP 或 NodePort 來確保服務之間可以相互連接。
- Pod 縮放：當擴展 FastAPI 應用時，確保 MongoDB 和 Redis 能夠應對多個副本的請求。