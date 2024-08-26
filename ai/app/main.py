from fastapi import FastAPI
from app.api.endpoints import infos
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(infos.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)