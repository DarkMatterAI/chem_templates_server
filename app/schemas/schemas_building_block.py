from typing import Union, Optional
from pydantic import BaseModel

from .schemas_common import (
#                             FilterRange, 
#                             IncludeCatalog, 
#                             SmartsFilters, 
                            TemplateConfig,
#                             TemplateEvalResponse
                            )

class ComputeSynthonRequest(BaseModel):
    inputs: list[str]

class SynthonData(BaseModel):
    synthon: str
    reaction_tags: list[str]

class ComputeSynthonResponse(BaseModel):
    input: str
    index: int
    valid_input: bool 
    synthons: list[SynthonData]


class BBAssemblySchema(BaseModel):
    template_config: TemplateConfig

class ProductAssemblySchema(BaseModel):
    reaction_mechanisms: dict[str, bool]
    template_config: TemplateConfig 

class AssemblySchema2BB(BaseModel):
    building_block_1: BBAssemblySchema
    building_block_2: BBAssemblySchema
    product: ProductAssemblySchema

class AssemblySchema3BB(BaseModel):
    building_block_1: BBAssemblySchema
    building_block_2: BBAssemblySchema
    intermediate_product_1: ProductAssemblySchema
    building_block_3: BBAssemblySchema
    product: ProductAssemblySchema


class AssemblyInputs2BB(BaseModel):
    building_block_1_inputs: list[str]
    building_block_2_inputs: list[str]

class AssemblyInputs3BB(AssemblyInputs2BB):
    building_block_3_inputs: list[str]


class AssemblyRequest2BB(BaseModel):
    assembly_schema: AssemblySchema2BB
    assembly_inputs: AssemblyInputs2BB

class AssemblyRequest3BB(BaseModel):
    assembly_schema: AssemblySchema3BB
    assembly_inputs: AssemblyInputs3BB
