from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
async def index():
    return JSONResponse(content={"msg":"I am Healthy."})