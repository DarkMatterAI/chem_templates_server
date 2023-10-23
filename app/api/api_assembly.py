from fastapi import APIRouter, responses
from typing import Union

from ..crud import crud_assembly as crud 
from ..schemas import schemas_assembly as schemas

router = APIRouter(default_response_class=responses.ORJSONResponse)

@router.post("/building_block/has_synthon", response_model=list[schemas.HasSynthonResponse])
async def compute_synthons_api(eval_request: schemas.HasSynthonRequest):
    results = await crud.has_synthon(eval_request)
    return results 

@router.post("/building_block/compute_synthons", response_model=list[schemas.ComputeSynthonResponse])
async def compute_synthons_api(eval_request: schemas.ComputeSynthonRequest):
    results = await crud.compute_synthons(eval_request)
    return results 

@router.get('/building_block/description')
def bb_description_api():
    return crud.bb_description()

@router.get('/building_block/reaction_mechanisms')
def get_rxn_mechanisms_api():
    return crud.get_rxn_mechanisms()

@router.post('/building_block/2bb_assembly', response_model=list[dict])
async def assemble_2bbs_api(assembly_inputs: schemas.TwoBBAseemblyRequest):
    results = await crud.assemble_2bbs(assembly_inputs)
    return results

@router.post('/building_block/3bb_assembly', response_model=list[dict])
async def assemble_2bbs_api(assembly_inputs: schemas.ThreeBBAseemblyRequest):
    results = await crud.assemble_3bbs(assembly_inputs)
    return results

@router.post('/building_block/custom_assembly', response_model=list[dict])
async def assemble_bb_custom_api(assembly_inputs: schemas.CustomAssemblySchema):
    results = await crud.assemble_custom(assembly_inputs, 'synthon')
    return results

@router.get('/fragment/description')
def frag_description_api():
    return crud.frag_description()

@router.post('/fragment/custom_assembly', response_model=list[dict])
async def assemble_frag_custom_api(assembly_inputs: schemas.CustomAssemblySchema):
    results = await crud.assemble_custom(assembly_inputs, 'fragment')
    return results

