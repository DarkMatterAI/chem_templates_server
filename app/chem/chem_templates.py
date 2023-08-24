import time
import logging
logger = logging.getLogger(__name__)

from .chem_imports import *


def range_check(range_dict):
    try: 
        valid_range = (range_dict['min_val'] is not None) or (range_dict['max_val'] is not None)
    except:
        logger.warning(f'bad filter range detected: {range_dict}')
        valid_range = False 
    return valid_range 

def validate_property_config(prop_name, filter_range):
    prop_check = (prop_name in PROP_FUNCS.keys())
    if prop_check and range_check(filter_range):
        return True
    else:
        if not prop_check:
            logger.warning(f'bad property spec detected: {prop_name}, {filter_range}')
        return False 

def validate_catalog_config(catalog_name, include_dict):
    catalog_check = (catalog_name in FILTER_CATALOGUES.keys())
    if catalog_check and include_dict['include']:
        return True 
    else:
        if not catalog_check:
            logger.warning(f'bad catalog spec detected: {catalog_name}, {include_dict}')
        return False 

def validate_smarts_config(smarts_string, filter_range):
    smarts_check = (smart_to_mol(smarts_string) is not None) 
    if smarts_check and range_check(filter_range):
        return True 
    else:
        if not smarts_check:
            logger.warning(f'bad smarts spec detected: {smarts_string}, {filter_range}')
        return False 

def strip_template(template_config):
    output = {
        'template_name' : template_config['template_name'],
        'property_filters' : {},
        'catalog_filters' : {},
        'smarts_filters' : {}
    }

    for prop_name, filter_range in template_config['property_filters'].items():
        if validate_property_config(prop_name, filter_range):
            output['property_filters'][prop_name] = filter_range

    for catalog_name, include_dict in template_config['catalog_filters'].items():
        if validate_catalog_config(catalog_name, include_dict):
            output['catalog_filters'][catalog_name] = include_dict

    for smarts_string, filter_range in template_config['smarts_filters'].items():
        if validate_smarts_config(smarts_string, filter_range):
            output['smarts_filters'][smarts_string] = filter_range

    return output 

class PropertyFilter(RangeFunctionFilter):
    def __init__(self, prop_func, prop_name, min_val=None, max_val=None):
        super().__init__(prop_func, prop_name, min_val, max_val)
        
    def __call__(self, molecule):
        value = self.func(molecule.mol)
        result = self.min_val <= value <= self.max_val
        data = {'min_val' : self.min_val, 'max_val' : self.max_val, 'value' : value}
        return FilterResult(result, self.name, data)

class RDCatalogFilter(Filter):
    def __init__(self, filter_catalog, name):
        self.filter_catalog = filter_catalog
        self.name = name
        
    def __call__(self, molecule):
        has_match = self.filter_catalog.HasMatch(molecule.mol)
        result = not has_match
        data = {'include' : True, 'has_match' : has_match}
        return FilterResult(result, self.name, data)


def build_property_filters(property_filter_dict):
    filters = []
    for prop_name, range_dict in property_filter_dict.items():
        if validate_property_config(prop_name, range_dict):
            f = PropertyFilter(PROP_FUNCS.get(prop_name), prop_name, 
                               min_val=range_dict['min_val'], max_val=range_dict['max_val'])
            f.filter_type = 'property_filters'
            filters.append(f)

    return filters 

def build_catalog_filters(catalog_filter_dict):
    filters = []
    for catalog_name, include_dict in catalog_filter_dict.items():
        if validate_catalog_config(catalog_name, include_dict):
            f = RDCatalogFilter(FILTER_CATALOGUES.get(catalog_name), catalog_name)
            f.filter_type = 'catalog_filters'
            filters.append(f)

    return filters 

def build_smarts_filters(smarts_filter_dict):
    filters = []
    for smarts_string, range_dict in smarts_filter_dict.items():
        if validate_smarts_config(smarts_string, range_dict):
            f = SimpleSmartsFilter(smarts_string, smarts_string, 
                                   min_val=range_dict['min_val'], max_val=range_dict['max_val'])
            f.filter_type = 'smarts_filters'
            filters.append(f)

    return filters

def build_filters(template_config):
    filters = []
    filters += build_property_filters(template_config['property_filters'])
    filters += build_catalog_filters(template_config['catalog_filters'])
    filters += build_smarts_filters(template_config['smarts_filters'])
    return filters 

def eval_query(query, filters, template_name, return_data=False):

    output = {
        'input' : query,
        'result' : True,
    }

    molecule = Molecule(query)

    if return_data:
        template_data = {
            'template_name' : template_name,
            'valid_input' : molecule.valid,
            'property_filters' : {},
            'catalog_filters' : {},
            'smarts_filters' : {}
        }
    else:
        template_data = None 

    if molecule.valid:
        for f in filters:
            result = f(molecule)
            output['result'] = output['result'] and result.filter_result

            if return_data:
                filter_data = result.filter_data
                filter_data['result'] = result.filter_result
                template_data[f.filter_type][f.name] = filter_data

            if (not return_data) and (not output['result']):
                # if not returning data, early exit on first failed filter
                output['template_data'] = None
                return output 

    else:
        output['result'] = False

    output['template_data'] = template_data 

    return output 

def run_request(queries, template_config, return_data=False):
    start = time.time()
    print(f'starting eval of {len(queries)} queries')

    filters = build_filters(template_config)

    results = [
                eval_query(i, filters, template_config['template_name'], return_data=return_data) 
                for i in queries
                ]

    elapsed = time.time() - start 
    print(f'finished eval of {len(queries)} queries in {elapsed} seconds')
    return results 

