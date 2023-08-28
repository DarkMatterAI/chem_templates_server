from fastapi import APIRouter, responses

from ..crud import crud_stateful as crud 
from ..schemas import schemas_stateful as schemas

router = APIRouter(default_response_class=responses.ORJSONResponse)

@router.on_event("startup")
async def init_db():
    await crud.init_mongodb()

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

@router.post("/building_block/2bb_assembly_stateful", response_model=list[dict])
async def assemble_2bbs_stateful_api(assembly_inputs: schemas.TwoBBAseemblyRequest):
    results = await crud.assemble_2bbs_stateful(assembly_inputs)
    return results

@router.post("/building_block/3bb_assembly_stateful", response_model=list[dict])
async def assemble_3bbs_stateful_api(assembly_inputs: schemas.ThreeBBAseemblyRequest):
    results = await crud.assemble_3bbs_stateful(assembly_inputs)
    return results

@router.post('/building_block/custom_assembly_stateful', response_model=list[dict])
async def assemble_bb_custom_stateful_api(assembly_inputs: schemas.CustomAssemblySchema):
    results = await crud.assemble_bb_custom_stateful(assembly_inputs, 'synthon')
    return results

@router.post('/fragment/custom_assembly_stateful', response_model=list[dict])
async def assemble_frag_custom_stateful_api(assembly_inputs: schemas.CustomAssemblySchema):
    results = await crud.assemble_frag_custom_stateful(assembly_inputs, 'fragment')
    return results




