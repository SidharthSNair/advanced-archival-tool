from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.core.config import app_info
from app.core.logging import configure_logging
from app.api.routes.health import router as health_router
from app.api.routes.regions import router as regions_router
from app.api.routes.nodes import router as nodes_router
from app.api.routes.archive import router as archive_router
from app.api.routes.admin import router as admin_router
from app.core.middleware import add_cors, add_security_headers, add_error_handler

# from fastapi.middleware.cors import CORSMiddleware


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

# origins = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

add_cors(app, origins=["http://localhost:5173"])
add_security_headers(app)
add_error_handler(app)

# Routers
app.include_router(health_router)
app.include_router(regions_router)
app.include_router(nodes_router)
app.include_router(archive_router)
app.include_router(admin_router)

for route in app.routes:
    print("🛣️", route.path)


# Convenience root
@app.get("/")
def root():
    return {"message": f"{app_info.name} is running", "version": app_info.version}
