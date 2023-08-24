from ..chem import chem_templates 
from ..schemas import schemas_functional as schemas 

def get_filter_descriptions():
    return chem_templates.FILTER_DESCRIPTIONS

def get_base_template():
    return chem_templates.BASE_TEMPLATE

def strip_template_crud(template_config: schemas.TemplateConfig):
    return chem_templates.strip_template(template_config.dict()) 

def eval_template_functional(eval_request: schemas.TemplateEvalRequestFunctional, return_data: bool):

    queries = eval_request.queries
    template_config = eval_request.template_config.dict()

    results = chem_templates.run_request(queries, template_config, return_data=return_data)

    return results
