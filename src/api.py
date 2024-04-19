import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from router.router_v1 import router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# 設定 CORS 標頭
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許的前端網域
    allow_credentials=True,
    allow_methods=["*"],  # 允許的 HTTP 方法
    allow_headers=["*"],  # 允許的 HTTP 標頭
)
app.include_router(router)

if __name__ == "__main__":
    load_dotenv()
    port = os.environ.get('PORT', 8000)
    uvicorn.run(app, host='0.0.0.0', workers=1, port=port)
