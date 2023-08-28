from fastapi.testclient import TestClient
import os 
import pytest
import copy

from app.tests.utils import *
from app.chem.chem_imports import BASE_TEMPLATE
from app.chem.chem_assembly import (BUILDING_BLOCK_ASSEMBLY_DESCRIPTION, 
                                    REACTION_MECHANISM_DICT,
                                    FRAGMENT_ASSEMBLY_DESCRIPTION)

def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200

##### template tests

def test_base_template(client: TestClient):
    response = client.get('/base_template')
    assert response.status_code == 200
    assert response.json() == BASE_TEMPLATE

def test_strip_template(client: TestClient):
    response = client.post('/strip_template', json=test_strip_template_input)
    assert response.status_code == 200
    assert response.json() == test_strip_template_output

def test_eval_template_functional_no_data(client: TestClient):
    response = client.post('eval_template_functional', 
                            json={'inputs' : test_smiles, 'template_config' : test_eval_template},
                            params={'return_data':False})
    assert response.status_code == 200
    assert response.json() == test_eval_template_results_no_data

def test_eval_template_functional_data(client: TestClient):
    response = client.post('eval_template_functional', 
                            json={'inputs' : test_smiles, 'template_config' : test_eval_template},
                            params={'return_data':True})
    assert response.status_code == 200
    assert response.json() == test_eval_template_results_data


##### stateful template tests

def _create_template_helper(template_config, client):
    response = client.post("/create_template", json=template_config)
    assert response.status_code == 200
    response_dict = response.json()
    template_id = response_dict['_id']
    assert response_dict['template_config'] == template_config
    return template_id 

def _read_template_helper(template_id, client):
    response = client.get(f"/get_template/{template_id}")
    assert response.status_code == 200
    response_dict = response.json()
    return response_dict 

def _update_template_helper(template_id, template_config, client):
    response = client.post(f"/update_template/{template_id}", json=template_config)
    assert response.status_code == 200
    response_dict = response.json()
    assert response_dict['template_config'] == template_config

def _delete_template_helper(template_id, client):
    response = client.delete(f"/delete_template/{template_id}")
    assert response.status_code == 200

def _skip_mongo():
    mongo_uri = os.environ.get('MONGO_URI', None)
    if (mongo_uri==None) or (mongo_uri==''):
        return True 
    return False 

@pytest.mark.skipif(_skip_mongo(), reason="mongodb connection not detected")
def test_template_stateful_api(client: TestClient):
    
    # create
    template_id = _create_template_helper(test_eval_template, client)

    # read
    response_dict = _read_template_helper(template_id, client)
    assert response_dict['template_config'] == test_eval_template

    # update
    _update_template_helper(template_id, test_eval_template_update, client)

    # delete
    _delete_template_helper(template_id, client)


@pytest.mark.skipif(_skip_mongo(), reason="mongodb connection not detected")
def test_eval_template_stateful_no_data(client: TestClient):
    template_id = _create_template_helper(test_eval_template, client)

    response = client.post(f"/eval_template_stateful/{template_id}",
                            json={'inputs':test_smiles}, params={'return_data':False})

    assert response.status_code == 200
    assert response.json() == test_eval_template_results_no_data

    _delete_template_helper(template_id, client)

@pytest.mark.skipif(_skip_mongo(), reason="mongodb connection not detected")
def test_eval_template_stateful_data(client: TestClient):
    template_id = _create_template_helper(test_eval_template, client)

    response = client.post(f"/eval_template_stateful/{template_id}",
                            json={'inputs':test_smiles}, params={'return_data':True})

    assert response.status_code == 200
    assert response.json() == test_eval_template_results_data

    _delete_template_helper(template_id, client)


##### assembly tests

def test_compute_synthon(client: TestClient):
    response = client.post('/building_block/compute_synthons', json=test_synthon_input)
    assert response.status_code == 200
    assert response.json() == test_synthon_output

def test_bb_description(client: TestClient):
    response = client.get('/building_block/description')
    assert response.status_code == 200
    assert response.json() == BUILDING_BLOCK_ASSEMBLY_DESCRIPTION

def test_rxn_description(client: TestClient):
    response = client.get('/building_block/reaction_mechanisms')
    assert response.status_code == 200
    assert response.json() == REACTION_MECHANISM_DICT

def test_2bb_assembly(client: TestClient):
    response = client.post('/building_block/2bb_assembly', json=test_2bb_inputs)
    assert response.status_code == 200
    assert response.json() == test_2bb_outputs

    new_inputs = copy.deepcopy(test_2bb_inputs)
    new_inputs['unmapped_inputs'] = unmapped_inputs
    response = client.post('/building_block/2bb_assembly', json=new_inputs)
    assert response.status_code == 200
    assert response.json() == test_2bb_outputs_unmapped

def test_3bb_assembly(client: TestClient):
    response = client.post('/building_block/3bb_assembly', json=test_3bb_inputs)
    assert response.status_code == 200
    assert response.json() == test_3bb_outputs

    new_inputs = copy.deepcopy(test_3bb_inputs)
    new_inputs['unmapped_inputs'] = unmapped_inputs
    response = client.post('/building_block/3bb_assembly', json=new_inputs)
    assert response.status_code == 200
    assert response.json() == test_3bb_outputs_unmapped

def test_bb_custom_assembly(client: TestClient):
    response = client.post('/building_block/custom_assembly', json=test_custom_bb_inputs)
    assert response.status_code == 200
    assert response.json() == test_custom_bb_outputs

    new_inputs = copy.deepcopy(test_custom_bb_inputs)
    new_inputs['unmapped_inputs'] = unmapped_inputs
    response = client.post('/building_block/custom_assembly', json=new_inputs)
    assert response.status_code == 200
    assert response.json() == test_custom_bb_outputs_unmapped

def test_fragment_description(client: TestClient):
    response = client.get('/fragment/description')
    assert response.status_code == 200
    assert response.json() == FRAGMENT_ASSEMBLY_DESCRIPTION

def test_frag_custom_assembly(client: TestClient):
    response = client.post('/fragment/custom_assembly', json=test_custom_frag_inputs)
    assert response.status_code == 200
    assert response.json() == test_custom_frag_outputs


##### stateful assembly tests

def _create_assembly_helper(assembly_schema, client):
    response = client.post("/create_assembly_schema", json={'assembly_schema' : assembly_schema})
    assert response.status_code == 200
    response_dict = response.json()
    schema_id = response_dict['_id']
    assert response_dict['assembly_schema'] == assembly_schema
    return schema_id

def _read_assembly_schema_helper(schema_id, client):
    response = client.get(f"/get_assembly_schema/{schema_id}")
    assert response.status_code == 200
    response_dict = response.json()
    return response_dict 

def _update_assembly_schema_helper(schema_id, assembly_schema, client):
    response = client.post(f"/update_assembly_schema/{schema_id}", json={'assembly_schema' : assembly_schema})
    assert response.status_code == 200
    response_dict = response.json()
    assert response_dict['assembly_schema'] == assembly_schema

def _delete_assembly_schema_helper(schema_id, client):
    response = client.delete(f"/delete_assembly_schema/{schema_id}")
    assert response.status_code == 200


@pytest.mark.skipif(_skip_mongo(), reason="mongodb connection not detected")
def test_assembly_crud_api(client: TestClient):

    schema = test_custom_bb_inputs['assembly_schema']
    
    # create
    schema_id = _create_assembly_helper(schema, client)

    # read
    response_dict = _read_assembly_schema_helper(schema_id, client)
    assert response_dict['assembly_schema'] == schema

    # update
    _update_assembly_schema_helper(schema_id, test_custom_frag_inputs['assembly_schema'], client)

    # delete
    _delete_assembly_schema_helper(schema_id, client)

@pytest.mark.skipif(_skip_mongo(), reason="mongodb connection not detected")
def test_2bb_assembly_stateful(client: TestClient):

    inputs = copy.deepcopy(test_2bb_inputs)
    template_id = _create_template_helper(inputs['building_block_1']['template_config'], client)

    inputs['building_block_1']['template_config'] = None 
    inputs['building_block_1']['template_id'] = template_id 
    inputs['building_block_2']['template_id'] = None 
    inputs['product']['template_id'] = None 


    response = client.post('/building_block/2bb_assembly_stateful', json=inputs)
    assert response.status_code == 200
    assert response.json() == test_2bb_outputs

    _delete_template_helper(template_id, client)

@pytest.mark.skipif(_skip_mongo(), reason="mongodb connection not detected")
def test_3bb_assembly_stateful(client: TestClient):

    inputs = copy.deepcopy(test_3bb_inputs)
    template_id = _create_template_helper(molwt_250_template, client)

    inputs['building_block_1']['template_id'] = template_id 

    inputs['building_block_2']['template_id'] = None 

    inputs['intermediate_product_1']['template_id'] = None 

    inputs['building_block_3']['template_id'] = None 

    inputs['product']['template_id'] = None 

    response = client.post('/building_block/3bb_assembly_stateful', json=inputs)
    assert response.status_code == 200
    assert response.json() == test_3bb_outputs

    _delete_template_helper(template_id, client)

@pytest.mark.skipif(_skip_mongo(), reason="mongodb connection not detected")
def test_bb_custom_assembly_stateful(client: TestClient):

    assembly_schema = test_custom_bb_inputs['assembly_schema']
    schema_id = _create_assembly_helper(assembly_schema, client)

    assembly_inputs = {
        'assembly_schema' : None,
        'assembly_schema_id' : schema_id,
        'mapped_inputs' : test_custom_bb_inputs['mapped_inputs'],
        'unmapped_inputs' : None
    }

    response = client.post('/building_block/custom_assembly_stateful', json=assembly_inputs)
    assert response.status_code == 200
    assert response.json() == test_custom_bb_outputs

    _delete_assembly_schema_helper(schema_id, client)

@pytest.mark.skipif(_skip_mongo(), reason="mongodb connection not detected")
def test_frag_custom_assembly_stateful(client: TestClient):

    assembly_schema = test_custom_frag_inputs['assembly_schema']
    schema_id = _create_assembly_helper(assembly_schema, client)

    assembly_inputs = {
        'assembly_schema' : None,
        'assembly_schema_id' : schema_id,
        'mapped_inputs' : test_custom_frag_inputs['mapped_inputs'],
        'unmapped_inputs' : test_custom_frag_inputs['unmapped_inputs']
    }

    response = client.post('/fragment/custom_assembly_stateful', json=assembly_inputs)
    assert response.status_code == 200
    assert response.json() == test_custom_frag_outputs

    _delete_assembly_schema_helper(schema_id, client)

