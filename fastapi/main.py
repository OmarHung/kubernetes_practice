import os

from fastapi import FastAPI
from pymongo import MongoClient
import redis


# 讀取環境變數
# MONGO_URL = os.getenv("MONGO_URL")
# REDIS_URL = os.getenv("REDIS_URL")
# print(MONGO_URL, REDIS_URL)

app = FastAPI()

# MongoDB 連接
# client = MongoClient(MONGO_URL)
# db = client["fastapi-db"]
# collection = db["test"]
#
# # 建立 Redis 連接
# r = redis.Redis.from_url(REDIS_URL)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# @app.get("/mongo")
# async def read_mongo():
#     collection.insert_one({"message": "Hello, MongoDB!"})
#     return {"message": "Inserted to MongoDB"}
#
# @app.get("/redis")
# async def read_redis():
#     r.set("message", "Hello, Redis!")
#     return {"message": r.get("message").decode("utf-8")}
