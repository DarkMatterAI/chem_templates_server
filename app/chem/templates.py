from .chem_imports import *
import logging
logger = logging.getLogger(__name__)

def _validate_input_helper(smile):
    output = {'input' : smile}
    mol = to_mol(smile)
    if mol is None:
        output['valid'] = False 
    else:
        output['valid'] = True 

    return output, mol

def compute_properties(smile, property_names):

    output, mol = _validate_input_helper(smile)

    if output['valid']:
        for prop in property_names:
            prop_func = PROP_FUNCS.get(prop, "property not found")

            if prop_func == "property not found":
                output[prop] = prop_func
            else:
                output[prop] = prop_func(mol)

    return output 


def compute_catalogs(smile, catalog_names):

    output, mol = _validate_input_helper(smile)

    if output['valid']:
        for cat_name in catalog_names:
            catalog = FILTER_CATALOGUES.get(cat_name, "catalog not found")

            if catalog == "catalog not found":
                output[cat_name] = catalog
            else:
                output[cat_name] = catalog.HasMatch(mol)

    return output 

def range_check(range_dict):
    try: 
        valid_range = (range_dict['min_val'] is not None) or (range_dict['max_val'] is not None)
    except:
        logger.warning('bad filter range detected')
        valid_range = False 
    return valid_range 

def strip_template(template_config):
    output = {
        'property_filters' : {},
        'catalog_filters' : {},
        'smarts_filters' : {}
    }

    for prop_name, filter_range in template_config['property_filters'].items():
        if prop_name in PROP_FUNCS.keys() and range_check(filter_range):
            output['property_filters'][prop_name] = filter_range 

    for cat_name, include in template_config['catalog_filters'].items():
        if cat_name in FILTER_CATALOGUES.keys() and include['include']:
            output['catalog_filters'][cat_name] = include 

    for smarts_string, filter_range in template_config['smarts_filters'].items():
        smarts_mol = smart_to_mol(smarts_string)

        if smarts_mol is None:
            logger.warning(f'bad filter smarts detected: {smarts_string}')
        
        if (smarts_mol is not None) and range_check(filter_range):
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
        prop_func = PROP_FUNCS.get(prop_name, None)

        if (prop_func is not None) and range_check(range_dict):
            f = PropertyFilter(prop_func, prop_name, min_val=range_dict['min_val'], max_val=range_dict['max_val'])
            f.filter_type = 'property_filters'
            filters.append(f)

    return filters 

def build_catalog_filters(catalog_filter_dict):
    filters = []
    for cat_name, include_dict in catalog_filter_dict.items():
        filter_catalog = FILTER_CATALOGUES.get(cat_name, None)

        if (filter_catalog is not None) and include_dict['include']:
            f = RDCatalogFilter(filter_catalog, cat_name)
            f.filter_type = 'catalog_filters'
            filters.append(f)

    return filters 

def build_smarts_filters(smarts_filter_dict):
    filters = []
    for smarts_string, range_dict in smarts_filter_dict.items():
        smarts_mol = smart_to_mol(smarts_string)

        if (smarts_mol is not None) and range_check(range_dict):
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

def eval_filters(smile, filters, minimal=False, early_exit=False):
    
    output = {
        'input' : smile,
        'result' : True,
    }
    
    if not minimal:
        output['valid_input'] = None
        output['property_filters'] = {}
        output['catalog_filters'] = {}
        output['smarts_filters'] = {}
    
    molecule = Molecule(smile)
    
    if not minimal:
        output['valid_input'] = molecule.valid
    
    if not molecule.valid:
        output['result'] = False
        return output
    
    output['result'] = True
    
    for f in filters:
        result = f(molecule)
        output['result'] = output['result'] and result.filter_result
        
        if not minimal:
            filter_data = result.filter_data
            filter_data['result'] = result.filter_result
            output[f.filter_type][f.name] = filter_data
            
        if early_exit and (not output['result']):
            return output
        
    return output
