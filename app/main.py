from fastapi import FastAPI, responses
from .config import CONFIG

from .api.api_functional import router as functional_router

app = FastAPI(default_response_class=responses.ORJSONResponse)

app.include_router(functional_router, tags=["functional"])

if CONFIG.MONGO_URI:
    from .api.api_stateful import router as stateful_router
    app.include_router(stateful_router, tags=["stateful"])

@app.get("/")
def read_root():
    return {"Hello": "World"}