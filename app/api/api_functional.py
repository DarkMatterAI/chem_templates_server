from fastapi import APIRouter, responses

from ..crud import crud_functional as crud 
from ..schemas import schemas_functional as schemas

router = APIRouter(default_response_class=responses.ORJSONResponse)

@router.get("/filter_descriptions")
def get_filter_descriptions_api():
    return crud.get_filter_descriptions()

@router.get("/base_template", response_model=schemas.TemplateConfig)
def get_base_template_api():
    return crud.get_base_template()

@router.post("/strip_template", response_model=schemas.TemplateConfig)
def strip_template_api(template_config: schemas.TemplateConfig):
    return crud.strip_template_crud(template_config)

@router.post("/eval_template_functional", response_model=list[schemas.TemplateEvalResponse])
def eval_template_functional_api(eval_request: schemas.TemplateEvalRequestFunctional, return_data: bool=True):
    return crud.eval_template_functional(eval_request, return_data)

