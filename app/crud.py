import time

from .schemas.filter_schemas import (
                                ComputePropertiesRequest, 
                                ComputeCatalogRequest,
                                TemplateConfig,
                                TemplateEvalRequest
                                )

from .chem.templates import (
                        PROPERTY_NAMES, 
                        CATALOG_NAMES, 
                        FILTER_DESCRIPTIONS,
                        BASE_TEMPLATE,
                        compute_properties, 
                        compute_catalogs,
                        strip_template,
                        build_filters,
                        eval_filters
                        )

def get_property_names():
    return {'property_names' : PROPERTY_NAMES}

def get_catalog_names_api():
    return {'catalog_names' : CATALOG_NAMES}

def compute_specific_values(items, names, default_names, compute_func):

    if (names is None) or (len(names)==0):
        names = default_names

    outputs = []
    for item in items:
        outputs.append(compute_func(item, names))
    
    return {'results' : outputs }

def compute_properties_crud(inputs: ComputePropertiesRequest):

    return compute_specific_values(inputs.queries, inputs.property_names, 
                                   PROPERTY_NAMES, compute_properties)

def compute_catalogs_crud(inputs: ComputeCatalogRequest):

    return compute_specific_values(inputs.queries, inputs.catalog_names, 
                                   CATALOG_NAMES, compute_catalogs)

def get_filter_descriptions():
    return FILTER_DESCRIPTIONS

def get_base_template():
    return BASE_TEMPLATE

def strip_template_crud(input_template: TemplateConfig):
    return strip_template(input_template.dict()) 

def eval_template(eval_request: TemplateEvalRequest, 
                  minimal: bool=True, 
                  early_exit: bool=True):
    start = time.time()

    queries = eval_request.queries
    template_config = eval_request.template_config.dict()

    print(f'starting eval with {len(queries)} queries')

    print(f'cleaning template')
    template_config = strip_template(template_config)

    print(f'building filters')
    filters = build_filters(template_config)

    outputs = []
    print(f'running queries')
    for query in queries:
        result = eval_filters(query, filters, minimal=minimal, early_exit=early_exit)
        outputs.append(result)


    elapsed = time.time() - start 
    print(f'finished eval in {elapsed} seconds')
    return outputs 