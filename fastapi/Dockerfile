FROM python:3.9-slim

# 設置了工作目錄，/app 目錄會在容器內部建立並被設置為當前的工作目錄。接下來的所有指令（例如 COPY 或 RUN）都會在這個目錄中執行。
WORKDIR /app

# 將 requirements.txt 複製到容器中的 /app 目錄中
COPY ../requirements.txt .

# 使用 pip 安裝 requirements.txt 中的所有依賴。
# --no-cache-dir 標誌防止 pip 緩存安裝的套件，這樣可以減少 Docker 映像的大小。
# RUN 指令會在容器建立時執行，這樣可以確保所有依賴都在容器中安裝好。
RUN pip install --no-cache-dir -r requirements.txt

# 將所有檔案複製到容器中的 /app 目錄中
COPY .. .

# 使用 CMD 指令指定容器啟動後要執行的命令
# CMD 指令可以有多個，但只有最後一個 CMD 指令會生效。
# 在啟動容器時，Docker 會執行 CMD 指令中的命令。
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
