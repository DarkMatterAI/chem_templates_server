import asyncio
from fastapi import HTTPException

from ..schemas import schemas_assembly as schemas
from ..chem import chem_assembly, chem_templates

async def compute_synthons(eval_request):

    inputs = eval_request.inputs
    results = chem_assembly.compute_synthons(inputs)

    await asyncio.sleep(0.01)

    return results 

def bb_description():
    return chem_assembly.BUILDING_BLOCK_ASSEMBLY_DESCRIPTION

def get_rxn_mechanisms():
    return chem_assembly.REACTION_MECHANISM_DICT

async def assemble_2bbs(assembly_inputs: schemas.TwoBBAseemblyRequest):

    results = chem_assembly.assemble_2bbs(assembly_inputs.dict())
    await asyncio.sleep(0.01)
    return results 

async def assemble_3bbs(assembly_inputs: schemas.ThreeBBAseemblyRequest):

    results = chem_assembly.assemble_3bbs(assembly_inputs.dict())
    await asyncio.sleep(0.01)
    return results 

async def assemble_bb_custom(assembly_inputs: schemas.CustomAssemblySchema):

    results = chem_assembly.assemble_bb_custom(assembly_inputs.dict())
    await asyncio.sleep(0.01)
    return results 



def frag_description():
    return chem_assembly.FRAGMENT_ASSEMBLY_DESCRIPTION



# def get_base_assembly_schema(schema_key):
#     schema_dict = {
#         '2bb' : chem_assembly.ASSEMBLY_SCHEMA_2BB,
#         '3bb' : chem_assembly.ASSEMBLY_SCHEMA_3BB
#     }

#     schema = schema_dict.get(schema_key, None)

#     if schema is None:
#         raise HTTPException(status_code=404, detail=f"template {template_id} not found")

#     return schema

# def strip_assembly_schema_crud(assembly_schema):

#     assembly_schema = chem_assembly.strip_assembly_schema(assembly_schema.dict())

#     return assembly_schema 



