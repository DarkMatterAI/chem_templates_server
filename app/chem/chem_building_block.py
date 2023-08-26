from .chem_imports import *
from .chem_templates import strip_template 
from chem_templates.building_blocks import (
                                            smile_to_synthon,
                                            REACTION_GROUP_NAMES
                                            )

def compute_synthons(inputs):
    results = []

    for i, item in enumerate(inputs):
        result = {
            'input' : item,
            'index' : i,
            'valid_input' : None,
            'synthons' : []
        }

        try:
            synthons, reaction_tags = smile_to_synthon(item)
            result['valid_input'] = True 
            result['synthons'] = [{'synthon' : synthons[j], 
                                   'reaction_tags' : reaction_tags[j]}
                                   for j in range(len(synthons))]

        except:
            result['valid_input'] = False 

        results.append(result)

    return results

def strip_assembly_schema(assembly_schema):

    for block_type, block_data in assembly_schema.items():
        if 'template_config' in block_data.keys():
            block_data['template_config'] = strip_template(block_data['template_config'])

        if 'reaction_mechanisms' in block_data.keys():
            block_data['reaction_mechanisms'] = {k:v for k,v in block_data['reaction_mechanisms'].items() if v}

    return assembly_schema 
