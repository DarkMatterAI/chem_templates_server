from .chem_imports import *
from .chem_templates import strip_template, build_filters
from chem_templates.building_blocks import (
                                            smile_to_synthon,
                                            REACTION_GROUP_NAMES
                                            )

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
        if k=='template_config':
            new_node_dict['template'] = config_to_template(v)
        elif k=='n_func':
            new_node_dict[k] = set(v)
        elif k=='reaction_mechanisms':
            new_node_dict['rxn_universe'] = config_to_rxn_universe(v)
        elif (k=='incoming_node') or (k=='next_node'):
            new_node_dict[k] = convert_assembly_schema(v)
        elif k=='children':
            new_node_dict[k] = [convert_assembly_schema(i) for i in v]
        else:
            new_node_dict[k] = v 

    return new_node_dict 

def run_assembly(assembly_schema, input_dict, assembly_type):

    assembly_inputs = AssemblyInputs(input_dict, 1000, 1e6, log=False)

    assembled = assembly_schema.assemble(assembly_inputs)

    outputs = [ASSEMBLY_TYPE_CONFIG[assembly_type]['assembly_schema_function'](i) 
                for i in assembled]

    if outputs:
        outputs = deduplicate_list(outputs, key_func=lambda x: x['result'])
        outputs = sorted(outputs, key=lambda x: x['result'])

    return outputs 

def assemble_inputs(assembly_input_dict, assembly_type):
    assembly_schema = assembly_input_dict['assembly_schema']
    mapped_inputs = assembly_input_dict['mapped_inputs']

    assembly_schema_dict = convert_assembly_schema(assembly_schema)

    assembly_schema = build_assembly_from_dict(assembly_schema_dict)

    input_dict = {}
    for k,v in mapped_inputs.items():
        input_dict[k] = process_inputs(v, assembly_type)

    return run_assembly(assembly_schema, input_dict, assembly_type)

def get_bb_leaf_node_schema(name, n_func, template_config):
    schema = {'name' : name,
              'node_type' : 'synthon_leaf_node',
              'n_func' : n_func,
              'template_config' : template_config}
    return schema 

def get_bb_product_node_schema(name, n_func, template_config, reaction_mechanisms, incoming_node, next_node):
    schema = {'name' : name, 
                'node_type' : 'synthon_node', 
                'n_func' : n_func,
                'template_config' : template_config,
                'reaction_mechanisms' : reaction_mechanisms,
                'incoming_node' : incoming_node,
                'next_node' : next_node}
    return schema 

def assemble_2bbs(assembly_inputs):
    bb1_schema = assembly_inputs['building_block_1']
    bb2_schema = assembly_inputs['building_block_2']
    product_schema = assembly_inputs['product']

    block1 = get_bb_leaf_node_schema('building_block_1', [1], bb1_schema['template_config'])

    block2 = get_bb_leaf_node_schema('building_block_2', [1], bb2_schema['template_config'])

    product = get_bb_product_node_schema('product', [0], product_schema['template_config'],
                                        product_schema['reaction_mechanisms'], block1, block2)

    input_schema = {
                        'building_block_1' : bb1_schema['inputs'],
                        'building_block_2' : bb2_schema['inputs']
                    }

    assembly_input_dict = {'assembly_schema' : product, 'mapped_inputs' : input_schema}

    return assemble_inputs(assembly_input_dict, 'synthon')


def assemble_3bbs(assembly_inputs):

    bb1_schema = assembly_inputs['building_block_1']
    bb2_schema = assembly_inputs['building_block_2']
    ip1_schema = assembly_inputs['intermediate_product_1']
    bb3_schema = assembly_inputs['building_block_3']
    product_schema = assembly_inputs['product']

    block1 = get_bb_leaf_node_schema('building_block_1', [1], bb1_schema['template_config'])

    block2 = get_bb_leaf_node_schema('building_block_2', [2], bb2_schema['template_config'])

    ip1 = get_bb_product_node_schema('intermediate_product_1', [1], ip1_schema['template_config'],
                                        ip1_schema['reaction_mechanisms'], block1, block2)

    block3 = get_bb_leaf_node_schema('building_block_3', [1], bb3_schema['template_config'])

    product = get_bb_product_node_schema('product', [0], product_schema['template_config'],
                                        product_schema['reaction_mechanisms'], ip1, block3)

    input_schema = {
                        'building_block_1' : bb1_schema['inputs'],
                        'building_block_2' : bb2_schema['inputs'],
                        'building_block_3' : bb3_schema['inputs']
                    }

    assembly_input_dict = {'assembly_schema' : product, 'mapped_inputs' : input_schema}

    return assemble_inputs(assembly_input_dict, 'synthon')

