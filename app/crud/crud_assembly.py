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

    results = chem_assembly.assemble_inputs(assembly_inputs.dict(), 'synthon')
    await asyncio.sleep(0.01)
    return results 

async def assemble_frag_custom(assembly_inputs: schemas.CustomAssemblySchema):

    results = chem_assembly.assemble_inputs(assembly_inputs.dict(), 'fragment')
    await asyncio.sleep(0.01)
    return results 



def frag_description():
    return chem_assembly.FRAGMENT_ASSEMBLY_DESCRIPTION



