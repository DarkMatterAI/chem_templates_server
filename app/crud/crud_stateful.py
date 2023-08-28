from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi import HTTPException
import asyncio

from ..chem import chem_templates, chem_assembly
from ..schemas import schemas_stateful as schemas 
from ..config import CONFIG

if CONFIG.MONGO_URI:
    client = AsyncIOMotorClient(CONFIG.MONGO_URI)
else:
    client = None

async def init_mongodb():
    await init_beanie(database=client[CONFIG.MONGO_DB_NAME], 
                      document_models=[schemas.TemplateDocument, schemas.AssemblySchemaDocument])

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

    inputs = eval_request.inputs
    template_config = item.template_config.dict()

    results = chem_templates.run_request(inputs, template_config, return_data=return_data)

    return results 


async def create_assembly_schema(assembly_schema: schemas.CreateAssemblySchema):

    assembly_schema = assembly_schema.dict()['assembly_schema']
    new_item = schemas.AssemblySchemaDocument(assembly_schema=assembly_schema)
    new_item = await new_item.insert()
    return new_item

async def get_assembly_schema(assembly_schema_id: str):
    item = await schemas.AssemblySchemaDocument.get(assembly_schema_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"assembly schema {assembly_schema_id} not found")

    return item

async def scroll_assembly_schema(skip: int, limit: int):
    items = await schemas.AssemblySchemaDocument.find().skip(skip).limit(limit).to_list()
    return items 

async def update_assembly_schema(assembly_schema_id: str, assembly_schema: schemas.CreateAssemblySchema):
    assembly_schema = assembly_schema.dict()['assembly_schema']
    item = await get_assembly_schema(assembly_schema_id)
    await item.set({'assembly_schema' : assembly_schema})
    return item 

async def delete_assembly_schema(assembly_schema_id: str):
    item = await get_assembly_schema(assembly_schema_id)
    item = await item.delete()
    return {'success' : item.acknowledged}


async def swap_template(input_dict):
    for k,v in input_dict.items():
        if k=='template_id' and (v is not None):
            item = await get_template(v)
            template_config = item.template_config.dict()
            input_dict['template_config'] = template_config 

        if type(v)==dict:
            await swap_template(v)


async def assemble_2bbs_stateful(assembly_inputs: schemas.TwoBBAseemblyRequestStateful):

    assembly_inputs = assembly_inputs.dict()
    await swap_template(assembly_inputs)
    results = chem_assembly.assemble_2bbs(assembly_inputs)
    return results 

async def assemble_3bbs_stateful(assembly_inputs: schemas.ThreeBBAseemblyRequestStateful):

    assembly_inputs = assembly_inputs.dict()
    await swap_template(assembly_inputs)
    results = chem_assembly.assemble_3bbs(assembly_inputs)
    return results 

async def assemble_custom_stateful(assembly_inputs: schemas.CustomAssemblySchemaStateful, assembly_type):

    assembly_inputs = assembly_inputs.dict()

    if assembly_inputs['assembly_schema_id']:
        schema = await get_assembly_schema(assembly_inputs['assembly_schema_id'])
        assembly_inputs['assembly_schema'] = schema.dict()['assembly_schema']

    await swap_template(assembly_inputs)
    results = chem_assembly.assemble_inputs(assembly_inputs, assembly_type)
    return results 

