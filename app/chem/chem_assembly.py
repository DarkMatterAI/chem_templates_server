from .chem_imports import *
from .chem_templates import strip_template, build_filters
from chem_templates.building_blocks import (
                                            smile_to_synthon,
                                            REACTION_GROUP_NAMES,
                                            BBClassifier
                                            )
from collections import defaultdict 

ASSEMBLY_TYPE_CONFIG = {
    'synthon' : {
                    'assembly_pool' : SynthonPool,
                    'assembly_schema_function' : build_synthesis_scheme
                },
    'fragment' : {
                    'assembly_pool' : AssemblyPool,
                    'assembly_schema_function' : build_fragment_assembly_scheme
                }
}


SCHEMA_REMAPPING_FUNCTIONS = {
    'template_config' : lambda k,v: ('template', config_to_template(v)),
    'n_func' : lambda k,v: (k, set(v)),
    'reaction_mechanisms' : lambda k,v: ('rxn_universe', config_to_rxn_universe(v)),
    'incoming_node' : lambda k,v: (k, convert_assembly_schema(v)),
    'next_node' : lambda k,v: (k, convert_assembly_schema(v)),
    'children' : lambda k,v: (k, [convert_assembly_schema(i) for i in v])
}

def has_synthon(inputs):
    results = []
    for i, item in enumerate(inputs):
        result = {
            'input' : item,
            'index' : i,
            'valid_input' : None,
            'has_synthon' : False 
        }
        mol = to_mol(item)
        if mol is None:
            result['valid_input'] = False
            result['has_synthon'] = False
        else:
            classes = BBClassifier(mol=mol)
            result['valid_input'] = True
            result['has_synthon'] = bool(classes)

        results.append(result)

    return results 

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
            result['synthons'] = [{'synthon' : synthons[j], 'reaction_tags' : reaction_tags[j]}
                                   for j in range(len(synthons))]

        except:
            result['valid_input'] = False 

        results.append(result)

    return results

def config_to_template(template_config):
    if template_config:
        filters = build_filters(template_config)
        template = Template(filters)
    else:
        template = None 
    return template 

def config_to_rxn_universe(rxn_mechanism_dict):
    reaction_mechanisms = [REACTION_GROUP_DICT[k] for k,v in rxn_mechanism_dict.items() if v]
    rxn_universe = ReactionUniverse('reactions', reaction_mechanisms)
    return rxn_universe 

def process_inputs(inputs, assembly_type):
    inputs = [Molecule(i['input'], data=i['data']) for i in inputs]

    if assembly_type == 'synthon':
        inputs = flatten_list([molecule_to_synthon(i) for i in inputs])

    inputs = deduplicate_list(inputs, key_func=lambda x: x.smile)
    inputs = ASSEMBLY_TYPE_CONFIG[assembly_type]['assembly_pool'](inputs)

    return inputs 

def convert_assembly_schema(node_dict):
    new_node_dict = {}
    for k,v in node_dict.items():
        convert_func = SCHEMA_REMAPPING_FUNCTIONS.get(k, lambda k,v: (k,v))
        new_k, new_v = convert_func(k,v)
        new_node_dict[new_k] = new_v 
    return new_node_dict 

def build_assembly_inputs(assembly_schema, mapped_inputs, unmapped_inputs, assembly_type):
    input_dict1 = {}
    input_dict2 = {}
    if mapped_inputs:
        for k,v in mapped_inputs.items():
            input_dict1[k] = process_inputs(v, assembly_type)

    if unmapped_inputs:
        unmapped_inputs = process_inputs(unmapped_inputs, assembly_type)
        input_dict2 = assembly_schema.build_assembly_pools(unmapped_inputs)

    merge_dict = defaultdict(list)
    for input_dict in [input_dict1, input_dict2]:
        for k,v in input_dict.items():
            merge_dict[k] += v.items

    input_dict = {k : ASSEMBLY_TYPE_CONFIG[assembly_type]['assembly_pool'](v) for k,v in merge_dict.items()}

    assembly_inputs = AssemblyInputs(input_dict, 1000, 1e6, log=False)

    return assembly_inputs 

def assemble_inputs(assembly_input_dict, assembly_type):
    assembly_schema = assembly_input_dict['assembly_schema']
    mapped_inputs = assembly_input_dict['mapped_inputs']
    unmapped_inputs = assembly_input_dict['unmapped_inputs']

    assembly_schema_dict = convert_assembly_schema(assembly_schema)

    assembly_schema = build_assembly_from_dict(assembly_schema_dict)

    assembly_inputs = build_assembly_inputs(assembly_schema, mapped_inputs, unmapped_inputs, assembly_type)

    assembled = assembly_schema.assemble(assembly_inputs)

    outputs = [ASSEMBLY_TYPE_CONFIG[assembly_type]['assembly_schema_function'](i) for i in assembled]

    if outputs:
        outputs = deduplicate_list(outputs, key_func=lambda x: x['result'])
        outputs = sorted(outputs, key=lambda x: x['result'])

    return outputs 

def get_bb_leaf_node_schema(assembly_inputs, name, n_func):
    node_schema = assembly_inputs[name]
    schema = {'name' : name,
              'node_type' : 'synthon_leaf_node',
              'n_func' : n_func,
              'template_config' : node_schema['template_config']}
    return schema 

def get_bb_product_node_schema(assembly_inputs, name, n_func, incoming_node, next_node):
    node_schema = assembly_inputs[name]
    schema = {'name' : name, 
                'node_type' : 'synthon_node', 
                'n_func' : n_func,
                'template_config' : node_schema['template_config'],
                'reaction_mechanisms' : node_schema['reaction_mechanisms'],
                'incoming_node' : incoming_node,
                'next_node' : next_node}
    return schema 

def get_mapped_inputs(assembly_inputs):
    mapped_inputs = {}
    for k,v in assembly_inputs.items():
        inputs = v.get('inputs', None)
        if inputs:
            mapped_inputs[k] = inputs 
    return mapped_inputs

def build_assembly_input_dict(assembly_inputs, assembly_schema):
    unmapped_inputs = assembly_inputs.pop('unmapped_inputs')
    mapped_inputs = get_mapped_inputs(assembly_inputs)
    assembly_input_dict = {'assembly_schema' : assembly_schema, 
                            'mapped_inputs' : mapped_inputs,
                            'unmapped_inputs' : unmapped_inputs}
    return assembly_input_dict

def assemble_2bbs(assembly_inputs):

    block1 = get_bb_leaf_node_schema(assembly_inputs, 'building_block_1', [1])
    block2 = get_bb_leaf_node_schema(assembly_inputs, 'building_block_2', [1])
    product = get_bb_product_node_schema(assembly_inputs, 'product', [0], block1, block2)

    assembly_input_dict = build_assembly_input_dict(assembly_inputs, product)

    return assemble_inputs(assembly_input_dict, 'synthon')

def assemble_3bbs(assembly_inputs):

    block1 = get_bb_leaf_node_schema(assembly_inputs, 'building_block_1', [1])
    block2 = get_bb_leaf_node_schema(assembly_inputs, 'building_block_2', [2])
    ip1 = get_bb_product_node_schema(assembly_inputs, 'intermediate_product_1', [1], block1, block2)
    block3 = get_bb_leaf_node_schema(assembly_inputs, 'building_block_3', [1])
    product = get_bb_product_node_schema(assembly_inputs, 'product', [0], ip1, block3)

    assembly_input_dict = build_assembly_input_dict(assembly_inputs, product)

    return assemble_inputs(assembly_input_dict, 'synthon')
