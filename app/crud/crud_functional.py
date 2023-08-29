import asyncio

from ..chem import chem_templates 
from ..schemas import schemas_functional as schemas 

def get_filter_descriptions():
    return chem_templates.FILTER_DESCRIPTIONS

def get_base_template():
    return chem_templates.BASE_TEMPLATE

def strip_template_crud(template_config: schemas.TemplateConfig):
    return chem_templates.strip_template(template_config.model_dump()) 

async def eval_template_functional(eval_request: schemas.TemplateEvalRequestFunctional, return_data: bool):

    inputs = eval_request.inputs
    template_config = eval_request.template_config.model_dump()

    results = chem_templates.run_request(inputs, template_config, return_data=return_data)
    
    await asyncio.sleep(0.01)

    return results
