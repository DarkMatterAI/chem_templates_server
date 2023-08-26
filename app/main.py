from fastapi import FastAPI, responses
from .config import CONFIG

from .api.api_functional import router as functional_router
from .api.api_building_block import router as bb_router

app = FastAPI(default_response_class=responses.ORJSONResponse)

app.include_router(functional_router, tags=["functional"])

if CONFIG.MONGO_URI:
    from .api.api_stateful import router as stateful_router
    app.include_router(stateful_router, tags=["stateful"])

app.include_router(bb_router, tags=["building_block"])

@app.get("/")
def read_root():
    return {"Hello": "World"}