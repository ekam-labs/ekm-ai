from app.schemas import ChatRequest
from app.services.router import route_model
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

app = FastAPI()

# Rate Limiter Setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


# Custom Rate Limit Handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please slow down."},
    )


# Main Chat Endpoint
@app.post("/chat")
@limiter.limit("10/minute")
async def chat(
    request: Request,
    req: ChatRequest,
):

    try:
        reply = route_model(
            req.model,
            req.messages,
        )
        return {"res": reply}

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
