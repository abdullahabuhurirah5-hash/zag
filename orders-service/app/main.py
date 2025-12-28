from fastapi import FastAPI

from app.api.routes.orders import orders_router
from app.db.init_db import init_db


def create_app() -> FastAPI:
    app = FastAPI(title="orders-service")
    app.include_router(orders_router, prefix="/api/v1")

    @app.on_event("startup")
    async def on_startup() -> None:
        # Create tables on startup (development convenience)
        await init_db()

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
