from .chem_imports import *
from .chem_templates import strip_template, build_filters
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

def config_to_template(template_config):
    if template_config:
        filters = build_filters(template_config)
        template = Template(filters)
    else:
        template = None 
    return template 

def config_to_rxn_universe(rxn_mechanism_dict):
    reaction_mechanisms = [REACTION_GROUP_DICT[k] for k,v in rxn_mechanism_dict.items() if v]
    print(f'found {len(reaction_mechanisms)} reaction mechanisms')
    rxn_universe = ReactionUniverse('reactions', reaction_mechanisms)
    return rxn_universe 

def inputs_to_synthons(inputs):
    molecules = [Molecule(i['input'], data=i['data']) for i in inputs]
    synthons = deduplicate_list(flatten_list([molecule_to_synthon(i) for i in molecules]), 
                            key_func=lambda x: x.smile)
    return synthons 

def convert_bb_leaf_node_request(node_dict, node_name, n_func):
    # inputs = node_dict['inputs']
    # molecules = [Molecule(i['input'], data=i['data']) for i in inputs]
    # synthons = deduplicate_list(flatten_list([molecule_to_synthon(i) for i in molecules]), 
    #                         key_func=lambda x: x.smile)

    synthons = inputs_to_synthons(node_dict['inputs'])

    node_schema = {
                    'name' : node_name,
                    'node_type' : 'synthon_leaf_node',
                    'n_func' : n_func,
                    'template_config' : node_dict['template_config']
                }

    return node_schema, synthons 

def convert_bb_product_node_request(node_dict, node_name, n_func, incoming_node, next_node):
    node_schema = {
                    'name' : node_name, 
                    'node_type' : 'synthon_node', 
                    'n_func' : n_func,
                    'template_config' : node_dict['template_config'],
                    'reaction_mechanisms' : node_dict['reaction_mechanisms'],
                    'incoming_node' : incoming_node,
                    'next_node' : next_node
                }
    return node_schema 

def convert_bb_assembly_schema(node_dict):
    if node_dict['node_type'] == 'synthon_node':
        new_node_dict = {
                        'name' : node_dict['name'], 
                        'node_type' : 'synthon_node', 
                        'n_func' : set(node_dict['n_func']),
                        'template' : config_to_template(node_dict['template_config']),
                        'rxn_universe' : config_to_rxn_universe(node_dict['reaction_mechanisms']),
                        'incoming_node' : convert_bb_assembly_schema(node_dict['incoming_node']),
                        'next_node' : convert_bb_assembly_schema(node_dict['next_node'])
                    }
    elif node_dict['node_type'] == 'synthon_leaf_node':
        new_node_dict = {
                            'name' : node_dict['name'], 
                            'node_type' : 'synthon_leaf_node',
                            'n_func' : set(node_dict['n_func']),
                            'template' : config_to_template(node_dict['template_config']),
                        }

    return new_node_dict 

def run_bb_assembly(assembly_schema, input_dict):

    assembly_inputs = AssemblyInputs(input_dict, 1000, 1000, log=False)

    assembled = assembly_schema.assemble(assembly_inputs)

    outputs = [build_synthesis_scheme(i) for i in assembled]

    return outputs 

def assemble_2bbs(assembly_inputs):

    block1, synthons1 = convert_bb_leaf_node_request(
                                        assembly_inputs['building_block_1'], 
                                        'building_block_1',
                                        [1]
                                        )

    block2, synthons2 = convert_bb_leaf_node_request(
                                        assembly_inputs['building_block_2'], 
                                        'building_block_2',
                                        [1]
                                        )

    product = convert_bb_product_node_request(
                                        assembly_inputs['product'],
                                        'product',
                                        [0],
                                        block1,
                                        block2
                                        )

    print(product)

    assembly_schema_dict = convert_bb_assembly_schema(product)

    assembly_schema = build_assembly_from_dict(assembly_schema_dict)

    input_dict = {
                'building_block_1' : SynthonPool(synthons1),
                'building_block_2' : SynthonPool(synthons2)
            }

    return run_bb_assembly(assembly_schema, input_dict)

def assemble_3bbs(assembly_inputs):

    block1, synthons1 = convert_bb_leaf_node_request(
                                        assembly_inputs['building_block_1'], 
                                        'building_block_1',
                                        [1]
                                        )

    block2, synthons2 = convert_bb_leaf_node_request(
                                        assembly_inputs['building_block_2'], 
                                        'building_block_2',
                                        [2]
                                        )

    intermediate_product_1 = convert_bb_product_node_request(
                                        assembly_inputs['intermediate_product_1'],
                                        'intermediate_product_1',
                                        [1],
                                        block1,
                                        block2
                                        )

    block3, synthons3 = convert_bb_leaf_node_request(
                                        assembly_inputs['building_block_3'], 
                                        'building_block_3',
                                        [1]
                                        )

    product = convert_bb_product_node_request(
                                        assembly_inputs['product'],
                                        'product',
                                        [0],
                                        intermediate_product_1,
                                        block3
                                        )

    print(product)

    assembly_schema_dict = convert_bb_assembly_schema(product)

    assembly_schema = build_assembly_from_dict(assembly_schema_dict)

    input_dict = {
                'building_block_1' : SynthonPool(synthons1),
                'building_block_2' : SynthonPool(synthons2),
                'building_block_3' : SynthonPool(synthons3),
            }

    return run_bb_assembly(assembly_schema, input_dict)


def assemble_bb_custom(assembly_input_dict):
    assembly_schema = assembly_input_dict['assembly_schema']
    input_schema = assembly_input_dict['input_schema']

    assembly_schema_dict = convert_bb_assembly_schema(assembly_schema)

    assembly_schema = build_assembly_from_dict(assembly_schema_dict)

    input_dict = {}
    for k,v in input_schema.items():
        synthons = inputs_to_synthons(v)
        input_dict[k] = SynthonPool(synthons)

    return run_bb_assembly(assembly_schema, input_dict)





