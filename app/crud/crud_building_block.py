import asyncio
from fastapi import HTTPException

from ..schemas import schemas_building_block as schemas
from ..chem import chem_building_block, chem_templates

def get_base_assembly_schema(schema_key):
    schema_dict = {
        '2bb' : chem_building_block.ASSEMBLY_SCHEMA_2BB,
        '3bb' : chem_building_block.ASSEMBLY_SCHEMA_3BB
    }

    schema = schema_dict.get(schema_key, None)

    if schema is None:
        raise HTTPException(status_code=404, detail=f"template {template_id} not found")

    return schema

def strip_assembly_schema_crud(assembly_schema):

    assembly_schema = chem_building_block.strip_assembly_schema(assembly_schema.dict())

    return assembly_schema 


async def compute_synthons(eval_request):

    inputs = eval_request.inputs
    results = chem_building_block.compute_synthons(inputs)

    await asyncio.sleep(0.01)

    return results 


