import uvicorn

from app import create_app
from config import config

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.api.run.host,
        port=config.api.run.port,
        reload=config.api.run.reload,
    )
