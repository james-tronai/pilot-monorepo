"""api-orders: a tiny orders service (MongoDB + Redis) used by the preview / DevSpace pilot.

Routes live under /api/orders so the same code works behind the Traefik path router in
preview and behind the Vite dev proxy in DevSpace, with no prefix stripping anywhere.
"""
import os
from datetime import datetime, timezone

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

GIT_SHA = os.getenv("GIT_SHA", "dev")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "pilot")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
REDIS_PREFIX = os.getenv("REDIS_PREFIX", "pilot:")

app = FastAPI(title="api-orders", root_path="")
mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo[MONGO_DB]
cache = redis.from_url(REDIS_URL, decode_responses=True)


class OrderIn(BaseModel):
    item: str
    qty: int = 1


@app.get("/api/orders/healthz")
async def healthz():
    return {"service": "api-orders", "sha": GIT_SHA, "mongoDb": MONGO_DB, "redisPrefix": REDIS_PREFIX}


@app.get("/api/orders")
async def list_orders():
    docs = await db.orders.find({}, {"_id": 0}).sort("createdAt", -1).to_list(100)
    return {"orders": docs, "count": await cache.get(f"{REDIS_PREFIX}orders:count") or "0"}


@app.post("/api/orders", status_code=201)
async def create_order(order: OrderIn):
    if order.qty < 1:
        raise HTTPException(400, "qty must be >= 1")
    doc = {"item": order.item, "qty": order.qty, "createdAt": datetime.now(timezone.utc).isoformat()}
    await db.orders.insert_one(dict(doc))
    await cache.incr(f"{REDIS_PREFIX}orders:count")
    return doc


@app.delete("/api/orders")
async def clear_orders():
    await db.orders.delete_many({})
    await cache.delete(f"{REDIS_PREFIX}orders:count")
    return {"ok": True}
