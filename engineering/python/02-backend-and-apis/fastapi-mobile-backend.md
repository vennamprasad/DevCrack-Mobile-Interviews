# ⚡ FastAPI Mobile Backend Blueprint

> **A production-grade, asynchronous backend guide for Mobile Engineers building high-throughput REST, SSE, and WebSocket services for iOS and Android clients.**

---

## 🎯 Why FastAPI for Mobile Backends?

| Feature | FastAPI (Python) | Node.js (Express) | Ktor / Spring (Kotlin) |
|:---|:---|:---|:---|
| **Async Performance** | Ultra-high (Starlette + Uvicorn) | High (Event loop) | High (Coroutines / Netty) |
| **Type Safety** | Pydantic v2 + Python Type Hints | TypeScript required | Native static typing |
| **API Docs (OpenAPI)** | Automatic Swagger & Redoc | Manual (Swagger JSDoc) | OpenAPI plugins required |
| **AI/ML Integration** | Native (PyTorch, LangChain, HuggingFace) | Via child processes | Via ONNX Runtime / JNI |

---

## 🏗️ Architecture for Mobile Clients

```
+-------------------------------------------------------+
|                Android / iOS Mobile App               |
+-------------------------------------------------------+
                           │
       (HTTPS REST / WSS WebSocket / SSE Stream)
                           ▼
+-------------------------------------------------------+
|               FastAPI Application Gateway             |
|  - Rate Limiting (SlowAPI)                            |
|  - JWT Header Extraction & Security Middleware        |
|  - Pydantic v2 Contract Validation                    |
+-------------------------------------------------------+
        │                                       │
        ▼                                       ▼
+-----------------------+              +-----------------------+
|  Async Database Pool  |              |  Redis Pub/Sub & Cache|
|  (SQLAlchemy 2.0 / PG)|              |  (Live sync & tokens) |
+-----------------------+              +-----------------------+
```

---

## 💻 1. Production FastAPI Mobile Service Template

```python
"""
Production FastAPI service with Pydantic validation, CORS for mobile web,
and structured JSON error responses.
"""
from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
import uuid

app = FastAPI(
    title="Mobile API Gateway",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# 1. CORS Configuration for Mobile Web / Local Simulators
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Pydantic v2 Contract Models for Mobile Clients
class DeviceInfo(BaseModel):
    platform: str = Field(..., example="iOS")  # 'iOS' | 'Android'
    os_version: str = Field(..., example="18.2")
    app_version: str = Field(..., example="2.4.0")
    device_model: str = Field(..., example="iPhone 16 Pro")

class FeedItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    title: str
    summary: str
    image_url: Optional[str] = None
    like_count: int = 0
    created_at_epoch_ms: int

class FeedResponse(BaseModel):
    items: List[FeedItem]
    next_cursor: Optional[str] = None
    has_more: bool

# 3. Mobile Header Extraction Dependency
async def verify_mobile_client(
    x_app_version: Optional[str] = Header(None),
    x_device_platform: Optional[str] = Header(None),
):
    if not x_device_platform:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing X-Device-Platform header (Required: 'iOS' | 'Android')",
        )
    return {"platform": x_device_platform, "version": x_app_version}

# 4. Paginated Feed Endpoint
@app.get("/api/v1/feed", response_model=FeedResponse)
async def get_mobile_feed(
    cursor: Optional[str] = None,
    limit: int = 20,
    client: dict = Depends(verify_mobile_client),
):
    # Simulated database fetch
    items = [
        FeedItem(
            id=str(uuid.uuid4()),
            title=f"Sample Engineering Post #{i}",
            summary="Clean mobile system design and architecture deep dive.",
            image_url="https://images.unsplash.com/photo-1555066931-4365d14bab8c",
            like_count=42 + i,
            created_at_epoch_ms=1710000000000,
        )
        for i in range(1, limit + 1)
    ]
    
    return FeedResponse(
        items=items,
        next_cursor=str(uuid.uuid4()),
        has_more=True,
    )
```

---

## 📡 2. Real-Time Streaming: Server-Sent Events (SSE)

For mobile live tickers, notification badges, and AI token streaming:

```python
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

@app.get("/api/v1/stream/tokens")
async def stream_ai_tokens(prompt: str):
    async def event_generator():
        tokens = ["Architecting", " high-scale", " mobile", " systems", " with", " FastAPI."]
        for token in tokens:
            await asyncio.sleep(0.15)  # Simulate LLM generation latency
            yield f"data: {token}\n\n"
        yield "event: end\ndata: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

---

## 🔐 3. Mobile JWT Refresh Token Rotation

In mobile architectures, store:
* **Access Token (Short-lived, e.g., 15 mins)**: In-memory or EncryptedSharedPreferences / iOS Keychain.
* **Refresh Token (Long-lived, e.g., 30 days)**: iOS Keychain / Android EncryptedSharedPreferences with biometric unlock.

```python
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your-secure-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: str, expires_delta: timedelta = timedelta(days=30)):
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": user_id, "exp": expire, "type": "refresh"}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

---

## 🚀 4. Running in Production with Uvicorn & Gunicorn

For maximum performance on multi-core servers:

```bash
# Development with hot-reload
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Production with 4 worker processes
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```
