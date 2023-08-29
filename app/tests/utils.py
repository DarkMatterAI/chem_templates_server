from app.chem.chem_assembly import REACTION_MECHANISM_DICT

test_strip_template_input = {
                            'template_name': 'test',
                            'property_filters': {
                                                'Molecular Weight': {'min_val': 250.0, 'max_val': 450.0},
                                                'Stereocenter Count': {'min_val': None, 'max_val': 1.0},
                                                'Rotatable Bonds': {'min_val': None, 'max_val': None},
                                                },
                            'catalog_filters': {
                                                'PAINS': {'include': True},
                                                'BRENK' : {'include' : False},
                                                'invalid_catalog' : {'include' : True}
                                                },
                            'smarts_filters': {
                                                'COS(=O)(=O)[C,c]': {'min_val': None, 'max_val': 0.0},
                                                'invalid_smarts': {'min_val': None, 'max_val': 0.0},
                                                'SC#N': {'min_val': None, 'max_val': None},
                                                }
                            }

test_strip_template_output = {
                            'template_name': 'test',
                            'property_filters': {
                                                'Molecular Weight': {'min_val': 250.0, 'max_val': 450.0},
                                                'Stereocenter Count': {'min_val': None, 'max_val': 1.0},
                                                },
                            'catalog_filters': {
                                                'PAINS': {'include': True},
                                                },
                            'smarts_filters': {
                                                'COS(=O)(=O)[C,c]': {'min_val': None, 'max_val': 0.0},
                                                }
                            }

test_eval_template = {
                    'template_name': 'test',
                    'property_filters': {'Molecular Weight': {'min_val': None, 'max_val': 100}},
                    'catalog_filters': {},
                    'smarts_filters': {}
                    }

test_eval_template_update = {
                    'template_name': 'test',
                    'property_filters': {'Molecular Weight': {'min_val': 50, 'max_val': 100}},
                    'catalog_filters': {},
                    'smarts_filters': {}
                    }

test_smiles = test_smiles = ['COC(=O)CCCNC(=O)Nc1cccc(Oc2ccccc2)c1', 'CCC', 'c']

test_eval_template_results_no_data = [{'input': 'COC(=O)CCCNC(=O)Nc1cccc(Oc2ccccc2)c1',
                                        'index' : 0,
                                        'result': False,
                                        'template_data': None},
                                        {'input': 'CCC', 'index' : 1, 'result': True, 'template_data': None},
                                        {'input': 'c', 'index' : 2, 'result': False, 'template_data': None}]

test_eval_template_results_data = [{'input': 'COC(=O)CCCNC(=O)Nc1cccc(Oc2ccccc2)c1',
                                    'index' : 0,
                                    'result': False,
                                    'template_data': {'template_name': 'test',
                                    'valid_input': True,
                                    'property_filters': {'Molecular Weight': {'min_val': None,
                                        'max_val': 100.0,
                                        'value': 328.14230712,
                                        'result': False}},
                                    'catalog_filters': {},
                                    'smarts_filters': {}}},
                                    {'input': 'CCC',
                                    'index' : 1,
                                    'result': True,
                                    'template_data': {'template_name': 'test',
                                    'valid_input': True,
                                    'property_filters': {'Molecular Weight': {'min_val': None,
                                        'max_val': 100.0,
                                        'value': 44.062600255999996,
                                        'result': True}},
                                    'catalog_filters': {},
                                    'smarts_filters': {}}},
                                    {'input': 'c',
                                    'index' : 2,
                                    'result': False,
                                    'template_data': {'template_name': 'test',
                                    'valid_input': False,
                                    'property_filters': {},
                                    'catalog_filters': {},
                                    'smarts_filters': {}}}]

test_synthon_input = {
                        "inputs": [
                            "COC(=O)c1cc2cc(F)ccc2cn1"
                        ]
                    }

test_synthon_output = [
                        {
                            "input": "COC(=O)c1cc2cc(F)ccc2cn1",
                            "index": 0,
                            "valid_input": True,
                            "synthons": [
                            {
                                "synthon": "O=[CH:10]c1cc2cc(F)ccc2cn1",
                                "reaction_tags": [
                                "Esters_Esters"
                                ]
                            }
                            ]
                        }
                    ]

bb1_template = {"template_name": "bb1_template",
                "property_filters": {"Molecular Weight": {"min_val": None, "max_val": 250}},
                "catalog_filters": {},
                "smarts_filters": {}}

bb2_template = {"template_name": "bb2_template",
                "property_filters": {
                "Molecular Weight": {"min_val": None, "max_val": 250}},
                "catalog_filters": {},
                "smarts_filters": {"[*]#[*]": {"min_val": None,"max_val": 0}}}

ro5_template = {"template_name": "ro5",
                "property_filters": {
                "LogP": {"min_val": None, "max_val": 5},
                "Molecular Weight": {"min_val": None, "max_val": 500},
                "Hydrogen Bond Donors": {"min_val": None, "max_val": 5},
                "Hydrogen Bond Acceptors": {"min_val": None, "max_val": 10}},
                "catalog_filters": {},
                "smarts_filters": {}}

molwt_250_template = {"template_name": "molwt_250",
                    "property_filters": {"Molecular Weight": {"min_val": None, "max_val": 250}},
                    "catalog_filters": {},
                    "smarts_filters": {}}

test_2bb_inputs = {
 "building_block_1": {
  "inputs": [{"input": "O=CC1CC2C(C1)C2(F)F", "data": {"ID": "EN300-7176480"}}],
  "template_config": bb1_template},
 "building_block_2": {
  "inputs": [{"input": "CC1CCCC(=CN(C)C)C1=O", "data": {"ID": "EN300-25308976"}},
             {"input": "N#Cc1cnn(-c2cccc(Br)c2)c1N", "data": {"ID": "EN300-110252"}}],
  "template_config": bb2_template},
 "product": {
  "reaction_mechanisms": REACTION_MECHANISM_DICT,
  "template_config": ro5_template},
 "unmapped_inputs": None
}

test_2bb_outputs = [{'result': 'CN(C)C=C1CCCC(C)(C(O)C2CC3C(C2)C3(F)F)C1=O', 'is_input': False,
    'assembly_data': {'parents': [
      {'input': 'O=CC1CC2C(C1)C2(F)F', 'is_input': True, 'data': {'ID': 'EN300-7176480'}},
      {'input': 'CC1CCCC(=CN(C)C)C1=O', 'is_input': True, 'data': {'ID': 'EN300-25308976'}}],
   'reaction_tags': ['Addition of Li, Mg, Zn organics to aldehydes and ketones']}}]

test_2bb_outputs_unmapped = [{'result': 'CN(C)C=C1CCCC(C)(C(O)C2CC3C(C2)C3(F)F)C1=O', 'is_input': False,
  'assembly_data': {'parents': [
      {'input': 'O=CC1CC2C(C1)C2(F)F', 'is_input': True, 'data': {'ID': 'EN300-7176480'}},
      {'input': 'CC1CCCC(=CN(C)C)C1=O', 'is_input': True, 'data': {'ID': 'EN300-25308976'}}],
   'reaction_tags': ['Addition of Li, Mg, Zn organics to aldehydes and ketones']}},
 {'result': 'COc1ccc(C)c(CN=CC2CC3C(C2)C3(F)F)n1', 'is_input': False,
  'assembly_data': {'parents': [
      {'input': 'O=CC1CC2C(C1)C2(F)F', 'is_input': True, 'data': {'ID': 'EN300-7176480'}},
      {'input': 'COc1ccc(C)c(CN)n1', 'is_input': True, 'data': {'source': 'unmaped'}}],
   'reaction_tags': ['Condensation of Y-NH2 with carbonyl compounds', 'Condensation of Y-NH2 with carbonyl compounds',
    'Condensation of Y-NH2 with carbonyl compounds', 'Condensation of Y-NH2 with carbonyl compounds']}},
 {'result': 'COc1ccc(C)c(CNC(O)C2CC3C(C2)C3(F)F)n1', 'is_input': False,
  'assembly_data': {'parents': [
      {'input': 'O=CC1CC2C(C1)C2(F)F', 'is_input': True, 'data': {'ID': 'EN300-7176480'}},
      {'input': 'COc1ccc(C)c(CN)n1', 'is_input': True, 'data': {'source': 'unmaped'}}],
   'reaction_tags': ['SN alkylation of amines']}},
 {'result': 'COc1ccc(C)c(CNC2C(=CN(C)C)CCCC2C)n1', 'is_input': False,
  'assembly_data': {'parents': [
      {'input': 'COc1ccc(C)c(CN)n1', 'is_input': True, 'data': {'source': 'unmaped'}},
      {'input': 'CC1CCCC(=CN(C)C)C1=O', 'is_input': True, 'data': {'ID': 'EN300-25308976'}}],
   'reaction_tags': ['SN alkylation of amines']}},
 {'result': 'COc1ccc(C)c(CNCC2CC3C(C2)C3(F)F)n1', 'is_input': False,
  'assembly_data': {'parents': [
      {'input': 'O=CC1CC2C(C1)C2(F)F', 'is_input': True, 'data': {'ID': 'EN300-7176480'}},
      {'input': 'COc1ccc(C)c(CN)n1', 'is_input': True, 'data': {'source': 'unmaped'}}],
   'reaction_tags': ['SN alkylation of amines']}}]

unmapped_inputs = [{'input':'COc1ccc(C)c(CN)n1', 'data' : {'source' : 'unmaped'}}]

test_3bb_inputs = {
  "building_block_1": {
    "inputs": [{"input": "CCOC(=O)c1c(N)ccnc1C(F)(F)F", "data": {"blah": "blee"}}],
    "template_config": None},
  "building_block_2": {
    "inputs": [{"input": "CCOC(=O)c1c(N)ccnc1C(F)(F)F","data": {"blah": "blee"}}],
    "template_config": None},
  "intermediate_product_1": {
    "reaction_mechanisms": {"N-acylation" : True, "Amine_alkylation_arylation" : True},
    "template_config": None},
  "building_block_3": {
    "inputs": [{"input": "COC(=O)C(C)N=C=O", "data": {"blah": "blee"}}],
    "template_config": None},
  "product": {
    "reaction_mechanisms": {"N-acylation" : True, "Amine_alkylation_arylation" : True},
    "template_config": None},
  "unmapped_inputs" : None}

test_3bb_outputs = [{'result': 'CC(NC(=O)Nc1ccnc(C(F)(F)F)c1C(=O)Nc1ccnc(C(F)(F)F)c1C(=O)O)C(=O)O', 'is_input': False,
  'assembly_data': {'parents': [
      {'result': 'O=C(O)c1c(NC(=O)c2c([NH2:20])ccnc2C(F)(F)F)ccnc1C(F)(F)F', 'is_input': False,
     'assembly_data': {'parents': [
         {'input': 'CCOC(=O)c1c(N)ccnc1C(F)(F)F', 'is_input': True, 'data': {'blah': 'blee'}},
         {'input': 'CCOC(=O)c1c(N)ccnc1C(F)(F)F', 'is_input': True, 'data': {'blah': 'blee'}}],
      'reaction_tags': ['Amine acylation']}},
      {'input': 'COC(=O)C(C)N=C=O', 'is_input': True, 'data': {'blah': 'blee'}}],
   'reaction_tags': ['N-Acylation by O=C(+)-X reagents (except isocyanates - R1.4)', 'Amine acylation by isocyanates or analogues']}}]

test_3bb_outputs_unmapped = [{'result': 'CC(NC(=O)Nc1ccnc(C(F)(F)F)c1C(=O)Nc1ccnc(C(F)(F)F)c1C(=O)O)C(=O)O', 'is_input': False,
  'assembly_data': {'parents': [
      {'result': 'O=C(O)c1c(NC(=O)c2c([NH2:20])ccnc2C(F)(F)F)ccnc1C(F)(F)F', 'is_input': False,
     'assembly_data': {'parents': [
         {'input': 'CCOC(=O)c1c(N)ccnc1C(F)(F)F', 'is_input': True, 'data': {'blah': 'blee'}},
         {'input': 'CCOC(=O)c1c(N)ccnc1C(F)(F)F', 'is_input': True, 'data': {'blah': 'blee'}}],
      'reaction_tags': ['Amine acylation']}},
      {'input': 'COC(=O)C(C)N=C=O', 'is_input': True, 'data': {'blah': 'blee'}}],
    'reaction_tags': ['N-Acylation by O=C(+)-X reagents (except isocyanates - R1.4)', 'Amine acylation by isocyanates or analogues']}},
 {'result': 'COc1ccc(C)c(CNC(=O)c2c(NC(=O)NC(C)C(=O)O)ccnc2C(F)(F)F)n1', 'is_input': False,
  'assembly_data': {'parents': [
      {'result': 'COc1ccc(C)c(CNC(=O)c2c([NH2:20])ccnc2C(F)(F)F)n1', 'is_input': False,
     'assembly_data': {'parents': [
         {'input': 'COc1ccc(C)c(CN)n1', 'is_input': True, 'data': {'source': 'unmaped'}},
         {'input': 'CCOC(=O)c1c(N)ccnc1C(F)(F)F', 'is_input': True, 'data': {'blah': 'blee'}}],
      'reaction_tags': ['Amine acylation']}},
      {'input': 'COC(=O)C(C)N=C=O', 'is_input': True, 'data': {'blah': 'blee'}}],
   'reaction_tags': ['N-Acylation by O=C(+)-X reagents (except isocyanates - R1.4)', 'Amine acylation by isocyanates or analogues']}}]

test_custom_bb_inputs = {
  "assembly_schema": {
        "name": "product",
        "node_type": "synthon_node",
        "n_func": [0], "template_config": None,
        "reaction_mechanisms": {"N-acylation": True, "Amine_sulphoacylation": False},
        "incoming_node": {
            "name": "building_block_1",
            "node_type": "synthon_leaf_node",
            "n_func": [1], "template_config": molwt_250_template
            },
        "next_node": {
            "name": "building_block_2",
            "node_type": "synthon_leaf_node",
            "n_func": [1], "template_config": None}},
  "mapped_inputs": {
    "building_block_1": [{"input": "COC(=O)C(C)N=C=O", "data": {"blah": "blee"}}],
    "building_block_2": [{"input": "CCN(C(=O)OCc1ccccc1)[C@@H]1CCN(C(=O)CN)C1", "data": {"blah": "bloo"}}]
  },
  "unmapped_inputs" : None
}

test_custom_bb_outputs = [{'result': 'CCNC1CCN(C(=O)CNC(=O)NC(C)C(=O)O)C1', 'is_input': False,
  'assembly_data': {'parents': [
      {'input': 'COC(=O)C(C)N=C=O', 'is_input': True, 'data': {'blah': 'blee'}},
      {'input': 'CCN(C(=O)OCc1ccccc1)[C@@H]1CCN(C(=O)CN)C1', 'is_input': True, 'data': {'blah': 'bloo'}}],
   'reaction_tags': ['N-Acylation by O=C(+)-X reagents (except isocyanates - R1.4)', 'Amine acylation by isocyanates or analogues']}}]

test_custom_bb_outputs_unmapped = [{'result': 'CCNC1CCN(C(=O)CNC(=O)NC(C)C(=O)O)C1', 'is_input': False,
  'assembly_data': {'parents': [
      {'input': 'COC(=O)C(C)N=C=O', 'is_input': True, 'data': {'blah': 'blee'}},
      {'input': 'CCN(C(=O)OCc1ccccc1)[C@@H]1CCN(C(=O)CN)C1', 'is_input': True, 'data': {'blah': 'bloo'}}],
   'reaction_tags': ['N-Acylation by O=C(+)-X reagents (except isocyanates - R1.4)',
    'Amine acylation by isocyanates or analogues']}},
 {'result': 'COc1ccc(C)c(CNC(=O)NC(C)C(=O)O)n1','is_input': False,
  'assembly_data': {'parents': [
      {'input': 'COC(=O)C(C)N=C=O', 'is_input': True, 'data': {'blah': 'blee'}},
      {'input': 'COc1ccc(C)c(CN)n1', 'is_input': True, 'data': {'source': 'unmaped'}}],
   'reaction_tags': ['N-Acylation by O=C(+)-X reagents (except isocyanates - R1.4)', 'Amine acylation by isocyanates or analogues']}}]

test_custom_frag_inputs = {'assembly_schema': {
    'name': 'full_molecule',
    'node_type': 'fragment_node',
    'template_config': None,
    'children': [{
        'name': 'R1',
        'node_type': 'fragment_leaf_node',
        'mapping_idxs': [1],
        'template_config': None},
        {'name': 'Linker',
        'node_type': 'fragment_leaf_node',
        'mapping_idxs': [1, 2],
        'template_config': None},
        {'name': 'Scaffold',
        'node_type': 'fragment_leaf_node',
        'mapping_idxs': [2],
        'template_config': None}]},
 'mapped_inputs': {'R1': [{'input': 'Cc1ccc(C[*])cc1', 'data': {}}]},
 'unmapped_inputs': [{'input': 'O=C(NC[*])[*]', 'data': {}},
  {'input': 'CC(=O)c1ccc(NC(=O)C[*])cc1', 'data': {}}]}

test_custom_frag_outputs = [{'result': 'CC(=O)c1ccc(NC(=O)CCNC(=O)CC(=O)Nc2ccc(C(C)=O)cc2)cc1', 'is_input': False,
  'assembly_data': {'parents': [
      {'input': 'CC(=O)c1ccc(NC(=O)C[*:1])cc1', 'is_input': True, 'data': {}},
      {'input': 'O=C(NC[*:2])[*:1]', 'is_input': True, 'data': {}},
      {'input': 'CC(=O)c1ccc(NC(=O)C[*:2])cc1', 'is_input': True, 'data': {}}],
   'input_smiles': 'CC(=O)c1ccc(NC(=O)C[*:1])cc1.O=C(NC[*:2])[*:1].CC(=O)c1ccc(NC(=O)C[*:2])cc1'}}]


