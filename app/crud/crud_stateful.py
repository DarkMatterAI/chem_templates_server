from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi import HTTPException

from ..chem import chem_templates 
from ..schemas import schemas_stateful as schemas 
from ..config import CONFIG

if CONFIG.MONGO_URI:
    client = AsyncIOMotorClient(CONFIG.MONGO_URI)
else:
    client = None

async def init_mongodb():
    await init_beanie(database=client[CONFIG.MONGO_DB_NAME], document_models=[schemas.TemplateDocument])

async def create_template(template_config: schemas.TemplateConfig):
    template_config = chem_templates.strip_template(template_config.dict())
    new_item = schemas.TemplateDocument(template_config=template_config)
    new_item = await new_item.insert()
    return new_item

async def get_template(template_id: str):
    item = await schemas.TemplateDocument.get(template_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"template {template_id} not found")

    return item

async def scroll_templates(skip: int, limit: int):
    items = await schemas.TemplateDocument.find().skip(skip).limit(limit).to_list()
    return items 

async def update_template(template_id: str, template_config: schemas.TemplateConfig):
    template_config = chem_templates.strip_template(template_config.dict())
    item = await get_template(template_id)
    await item.set({'template_config' : template_config})
    return item 

async def delete_template(template_id: str):
    item = await get_template(template_id)
    item = await item.delete()
    return {'success' : item.acknowledged}

async def eval_template_stateful(template_id: str, eval_request: schemas.EvalRequestStateful, return_data: bool=True):
    item = await get_template(template_id)

    queries = eval_request.queries
    template_config = item.template_config.dict()

    results = chem_templates.run_request(queries, template_config, return_data=return_data)

    return results 
