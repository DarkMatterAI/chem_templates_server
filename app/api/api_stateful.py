from fastapi import APIRouter, responses

from ..crud import crud_stateful as crud 
from ..schemas import schemas_stateful as schemas

router = APIRouter(default_response_class=responses.ORJSONResponse)

@router.on_event("startup")
async def init_db():
    await crud.init_mongodb()

##### templates 

@router.post("/create_template", response_model=schemas.TemplateDocument)
async def create_template_api(template_config: schemas.TemplateConfig):
    item = await crud.create_template(template_config)
    return item 

@router.get("/get_template/{template_id}", response_model=schemas.TemplateDocument)
async def get_template_api(template_id: str):
    item = await crud.get_template(template_id)
    return item 

@router.get("/scroll_templates", response_model=list[schemas.TemplateDocument])
async def scroll_templates_api(skip: int=0, limit: int=100):
    items = await crud.scroll_templates(skip, limit)
    return items 

@router.post("/update_template/{template_id}", response_model=schemas.TemplateDocument)
async def update_template_api(template_id: str, template_config: schemas.TemplateConfig):
    item = await crud.update_template(template_id, template_config)
    return item 

@router.delete("/delete_template/{template_id}")
async def delete_template_api(template_id: str):
    result = await crud.delete_template(template_id)
    return result

@router.post("/eval_template_stateful/{template_id}", response_model=list[schemas.TemplateEvalResponse])
async def eval_template_stateful_api(template_id: str, eval_request: schemas.EvalRequestStateful, return_data: bool=True):
    results = await crud.eval_template_stateful(template_id, eval_request, return_data)
    return results


##### assembly 

@router.post("/create_assembly_schema", response_model=schemas.AssemblySchemaDocument)
async def create_assembly_schema_api(assembly_schema: schemas.CreateAssemblySchema):
    item = await crud.create_assembly_schema(assembly_schema)
    return item 

@router.get("/get_assembly_schema/{assembly_schema_id}", response_model=schemas.AssemblySchemaDocument)
async def get_assembly_schema_api(assembly_schema_id: str):
    item = await crud.get_assembly_schema(assembly_schema_id)
    return item 

@router.get("/scroll_assembly_schema", response_model=list[schemas.AssemblySchemaDocument])
async def scroll_assembly_schema_api(skip: int=0, limit: int=100):
    items = await crud.scroll_assembly_schema(skip, limit)
    return items 

@router.post("/update_assembly_schema/{assembly_schema_id}", response_model=schemas.AssemblySchemaDocument)
async def update_assembly_schema_api(assembly_schema_id: str, assembly_schema: schemas.CreateAssemblySchema):
    item = await crud.update_assembly_schema(assembly_schema_id, assembly_schema)
    return item 

@router.delete("/delete_assembly_schema/{assembly_schema_id}")
async def delete_assembly_schema_api(assembly_schema_id: str):
    result = await crud.delete_assembly_schema(assembly_schema_id)
    return result

@router.post("/building_block/2bb_assembly_stateful", response_model=list[dict])
async def assemble_2bbs_stateful_api(assembly_inputs: schemas.TwoBBAseemblyRequestStateful):
    results = await crud.assemble_2bbs_stateful(assembly_inputs)
    return results

@router.post("/building_block/3bb_assembly_stateful", response_model=list[dict])
async def assemble_3bbs_stateful_api(assembly_inputs: schemas.ThreeBBAseemblyRequestStateful):
    results = await crud.assemble_3bbs_stateful(assembly_inputs)
    return results

@router.post('/building_block/custom_assembly_stateful', response_model=list[dict])
async def assemble_bb_custom_stateful_api(assembly_inputs: schemas.CustomAssemblySchemaStateful):
    results = await crud.assemble_custom_stateful(assembly_inputs, 'synthon')
    return results

@router.post('/fragment/custom_assembly_stateful', response_model=list[dict])
async def assemble_frag_custom_stateful_api(assembly_inputs: schemas.CustomAssemblySchemaStateful):
    results = await crud.assemble_custom_stateful(assembly_inputs, 'fragment')
    return results




