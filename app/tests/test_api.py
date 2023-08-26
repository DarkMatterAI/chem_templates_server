from fastapi.testclient import TestClient
import os 
import pytest

from app.chem.chem_imports import BASE_TEMPLATE

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


def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200

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


def _create_helper(template_config, client):
    response = client.post("/create_template", json=template_config)
    assert response.status_code == 200
    response_dict = response.json()
    template_id = response_dict['_id']
    assert response_dict['template_config'] == template_config
    return template_id 

def _read_helper(template_id, client):
    response = client.get(f"/get_template/{template_id}")
    assert response.status_code == 200
    response_dict = response.json()
    return response_dict 

def _update_helper(template_id, template_config, client):
    response = client.post(f"/update_template/{template_id}", json=template_config)
    assert response.status_code == 200
    response_dict = response.json()
    assert response_dict['template_config'] == template_config

def _delete_helper(template_id, client):
    response = client.delete(f"/delete_template/{template_id}")
    assert response.status_code == 200

def _skip_mongo():
    mongo_uri = os.environ.get('MONGO_URI', None)
    if (mongo_uri==None) or (mongo_uri==''):
        return True 
    return False 

@pytest.mark.skipif(_skip_mongo(), reason="mongodb connection not detected")
def test_stateful_api(client: TestClient):
    
    # create
    template_id = _create_helper(test_eval_template, client)

    # read
    response_dict = _read_helper(template_id, client)
    assert response_dict['template_config'] == test_eval_template

    # update
    _update_helper(template_id, test_eval_template_update, client)

    # delete
    _delete_helper(template_id, client)


@pytest.mark.skipif(_skip_mongo(), reason="mongodb connection not detected")
def test_eval_template_stateful_no_data(client: TestClient):
    template_id = _create_helper(test_eval_template, client)

    response = client.post(f"/eval_template_stateful/{template_id}",
                            json={'inputs':test_smiles}, params={'return_data':False})

    assert response.status_code == 200
    assert response.json() == test_eval_template_results_no_data

    _delete_helper(template_id, client)

@pytest.mark.skipif(_skip_mongo(), reason="mongodb connection not detected")
def test_eval_template_stateful_data(client: TestClient):
    template_id = _create_helper(test_eval_template, client)

    response = client.post(f"/eval_template_stateful/{template_id}",
                            json={'inputs':test_smiles}, params={'return_data':True})

    assert response.status_code == 200
    assert response.json() == test_eval_template_results_data

    _delete_helper(template_id, client)

