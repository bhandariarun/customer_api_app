"""
main.py — Application Entry Point
Creates the FastAPI app, mounts the customer router, and starts the server.
"""

from fastapi import FastAPI
from app.router.router import customer_router, dashboard_router
from app.logger.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="ClassicModels Customer API",
    description=(
        "A layered REST API for the ClassicModels database. "
        "Browse, create, update, and delete customer records — with related "
        "orders and payments included automatically."
    ),
    version="1.0.0",
    contact={"name": "Fusemachine Fellowship"},
    license_info={"name": "MIT"},
)

app.include_router(dashboard_router)
app.include_router(customer_router)

logger.info("ClassicModels Customer API started. Docs at /docs")


@app.get("/", tags=["Health"])
def health_check():
    """Quick sanity-check endpoint."""
    logger.info("GET / — health check called.")
    return {"status": "ok", "message": "Customer API is running. Visit /docs for the full API."}
