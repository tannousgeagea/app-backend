import uvicorn
from uuid import uuid4
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data_api.routers.images import get_images

def create_app() -> FastAPI:
    tags_meta = [
        {
            "name": "Image Upload DATA API",
            "description": "Image Upload data entrypoint API"
        }
    ]

    app = FastAPI(
        openapi_tags = tags_meta,
        debug=True,
        title="Image Upload data entrypoint API",
        summary="",
        version="0.0.1",
        contact={
            "name": "Tannous Geagea",
            "url": "https://wasteant.com",
            "email": "tannous.geagea@wasteant.com",            
        },
        openapi_url="/openapi.json"
    )

    origins = ["http://localhost:3000", "http://localhost:8085"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["X-Requested-With", "X-Request-ID"],
        expose_headers=["X-Request-ID"],
    )

    app.include_router(get_images.router)
    
    return app

app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8085, log_level="debug", reload=True)
