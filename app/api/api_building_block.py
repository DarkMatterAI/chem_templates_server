from fastapi import APIRouter, responses
from typing import Union

from ..crud import crud_building_block as crud 
from ..schemas import schemas_building_block as schemas

router = APIRouter(default_response_class=responses.ORJSONResponse)

@router.get("/base_assembly_schema_2bb", response_model=schemas.AssemblySchema2BB)
def get_base_assembly_schema_api():
    return crud.get_base_assembly_schema('2bb')

@router.get("/base_assembly_schema_3bb", response_model=schemas.AssemblySchema3BB)
def get_base_assembly_schema_api():
    return crud.get_base_assembly_schema('3bb')

@router.post("/strip_assembly_schema", response_model=schemas.AssemblySchema2BB)
def strip_assembly_schema_api(assembly_schema: Union[schemas.AssemblySchema2BB, schemas.AssemblySchema3BB]):
    return crud.strip_assembly_schema_crud(assembly_schema)

@router.post("/compute_synthons", response_model=list[schemas.ComputeSynthonResponse])
async def compute_synthons_api(eval_request: schemas.ComputeSynthonRequest):
    results = await crud.compute_synthons(eval_request)
    return results 


