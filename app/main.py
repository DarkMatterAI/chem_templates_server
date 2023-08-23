from fastapi import FastAPI, responses
import logging
logger = logging.getLogger(__name__)

from .schemas.filter_schemas import *

from . import crud 

app = FastAPI(default_response_class=responses.ORJSONResponse)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/property_names")
def get_property_names_api():
    return crud.get_property_names()

@app.get("/catalog_names")
def get_catalog_names_api():
    return crud.get_catalog_names_api()

@app.post("/compute_properties", response_model=ComputePropertiesResponse)
def compute_properties_api(inputs: ComputePropertiesRequest):
    return crud.compute_properties_crud(inputs)

@app.post("/compute_catalogs", response_model=ComputeCatalogResponse)
def compute_catalogs_api(inputs: ComputeCatalogRequest):
    return crud.compute_catalogs_crud(inputs)

@app.get("/filter_descriptions")
def get_filter_descriptions_api():
    return crud.get_filter_descriptions()

@app.get("/base_template", response_model=TemplateConfig)
def get_base_template_api():
    return crud.get_base_template()

@app.post("/strip_template", response_model=TemplateConfig)
def strip_template_api(input_template: TemplateConfig):
    return crud.strip_template_crud(input_template)

@app.post("/eval_template", response_model=list[TemplateEvalResponse])
def eval_template_api(eval_request: TemplateEvalRequest):
    return crud.eval_template(eval_request, minimal=True, early_exit=True)

@app.post("/eval_template_verbose", response_model=list[TemplateEvalResponseVerbose])
def eval_template_verbose_api(eval_request: TemplateEvalRequest):
    return crud.eval_template(eval_request, minimal=False, early_exit=False)
