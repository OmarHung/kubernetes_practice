
# Docker 基礎練習 - FastAPI、MongoDB 和 Redis

這是一份關於如何使用 Docker 容器化 FastAPI 應用程式，並結合 MongoDB 和 Redis 的教學文檔。通過這些練習，你將學會如何將應用程式放入容器，並了解容器化數據庫的基礎。

## 階段 1：Docker 基礎練習

### 1.1 建立 FastAPI 應用並容器化

#### 任務：建立一個簡單的 FastAPI 應用，將其容器化。

**步驟**：
1. **安裝 FastAPI 和 Uvicorn**：
    - 建立一個新的目錄來保存你的 FastAPI 應用：
      ```bash
      mkdir fastapi-app && cd fastapi-app
      ```
    - 創建一個虛擬環境並安裝依賴：
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      pip install fastapi uvicorn
      ```
    - 在 `main.py` 中寫入簡單的 FastAPI 應用程式：
      ```python
      from fastapi import FastAPI

      app = FastAPI()

      @app.get("/")
      async def read_root():
          return {"message": "Hello, Docker!"}
      ```
    - 測試本地運行：
      ```bash
      uvicorn main:app --reload --host 0.0.0.0 --port 8000
      ```

2. **撰寫 Dockerfile**：
    - 在根目錄創建一個 `Dockerfile` 文件：
      ```Dockerfile
      FROM python:3.9-slim

      WORKDIR /app

      COPY ../requirements.txt .
      RUN pip install --no-cache-dir -r requirements.txt

      COPY .. .

      CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
      ```
    - 生成 `requirements.txt`：
      ```bash
      pip freeze > requirements.txt
      ```

3. **構建和運行 Docker 映像**：
    - 構建映像：
      ```bash
      docker build -t fastapi-app .
      ```
    - 運行容器：
      ```bash
      docker run -d -p 8000:8000 fastapi-app
      ```

### 1.2 結合 MongoDB 和 Redis

#### 任務：將 FastAPI 應用連接到 MongoDB 和 Redis，並使用 Docker Compose 來管理多個服務。

**步驟**：
1. **安裝 MongoDB 和 Redis 驅動**：
    - 安裝所需的 Python 驅動：
      ```bash
      pip install pymongo redis
      ```

2. **更新 FastAPI 應用以使用 MongoDB 和 Redis**：
    - 在 `main.py` 中新增 MongoDB 和 Redis 的連接：
      ```python
      from fastapi import FastAPI
      from pymongo import MongoClient
      import redis

      app = FastAPI()

      # MongoDB 連接
      client = MongoClient("mongodb://mongo:27017/")
      db = client["fastapi-db"]
      collection = db["test"]

      # Redis 連接
      r = redis.Redis(host='redis', port=6379)

      @app.get("/mongo")
      async def read_mongo():
          collection.insert_one({"message": "Hello, MongoDB!"})
          return {"message": "Inserted to MongoDB"}

      @app.get("/redis")
      async def read_redis():
          r.set("message", "Hello, Redis!")
          return {"message": r.get("message").decode("utf-8")}
      ```

3. **撰寫 Docker Compose 文件**：
    - 創建一個 `docker-compose.yml` 文件來運行 FastAPI、MongoDB 和 Redis：
      ```yaml
      version: "3.8"
      services:
        app:
          build: .
          ports:
            - "8000:8000"
          depends_on:
            - mongo
            - redis
        mongo:
          image: mongo:latest
          ports:
            - "27017:27017"
        redis:
          image: redis:latest
          ports:
            - "6379:6379"
      ```
    - 使用 Docker Compose 啟動服務：
      ```bash
      docker-compose up --build
      ```

### 注意事項：
- **MongoDB 連接問題**：在容器間通訊時，需要使用服務名（如 `mongo` 而不是 `localhost`），這是 Docker Compose 提供的內部 DNS 功能。
- **持久化數據**：要將 MongoDB 或 Redis 的數據持久化，你需要在 Docker Compose 中定義卷。

---

## 問答部分

### 問題：`RUN` 跟 `CMD` 差在哪？ 為什麼 pip 安裝應用程式是用 `RUN` 而啟動 FastAPI 是用 `CMD`？

#### 解釋：

1. **`RUN`** 和 **`CMD`** 的區別：
   - **`RUN`**：用來在構建 Docker 映像時執行一次性的命令，結果會被保存到映像中。這些操作通常用於安裝應用所需的依賴、配置環境等。
   - **`CMD`**：用來指定容器啟動時要執行的默認命令。當你用 `docker run` 啟動容器時，`CMD` 會被執行，它用於定義容器運行時應該執行的長期進程。

2. **為什麼安裝依賴使用 `RUN`，啟動 FastAPI 使用 `CMD`**：
   - 安裝依賴是構建映像的過程，只需要執行一次，安裝完成後保存到 Docker 映像中，所以使用 `RUN`。
   - FastAPI 應用則需要在容器每次啟動時運行，作為應用的核心服務，因此使用 `CMD` 指定啟動指令。

---

## 總結

通過這一階段的練習，你可以學會如何：
- 創建和容器化 FastAPI 應用。
- 使用 Docker Compose 同時運行多個容器化服務（FastAPI、MongoDB、Redis）。
- 使用 `RUN` 來安裝應用依賴，並用 `CMD` 來啟動應用進程。
- 使用 `volumes` 在 Docker 中實現數據持久化。

學會這些概念後，你將能夠構建更加複雜的應用，並進一步探索 Kubernetes 的使用。
