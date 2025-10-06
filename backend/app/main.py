from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.core.config import app_info
from app.core.logging import configure_logging
from app.api.routes.health import router as health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    configure_logging()
    # You could test DB connectivity here if desired
    yield
    # Shutdown (cleanup) if needed later

app = FastAPI(
    title=app_info.name,
    version=app_info.version,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

# Routers
app.include_router(health_router)

# Convenience root
@app.get("/")
def root():
    return {"message": f"{app_info.name} is running", "version": app_info.version}
