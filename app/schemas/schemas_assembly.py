from typing import Union, Optional
from pydantic import BaseModel

from .schemas_common import TemplateConfig

class HasSynthonRequest(BaseModel):
    inputs: list[str]

class HasSynthonResponse(BaseModel):
    input: str 
    index: int 
    valid_input: bool 
    result: bool 

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


class AssemblyInputItem(BaseModel):
    input: str 
    data: dict 

class AssemblyLeafNodeInputs(BaseModel):
    inputs: list[AssemblyInputItem]
    template_config: Optional[TemplateConfig]

class ReactionNodeInputs(BaseModel):
    reaction_mechanisms: dict[str, bool]
    template_config: Optional[TemplateConfig]

class TwoBBAseemblyRequest(BaseModel):
    building_block_1: AssemblyLeafNodeInputs
    building_block_2: AssemblyLeafNodeInputs
    product: ReactionNodeInputs
    unmapped_inputs: Optional[list[AssemblyInputItem]]

class ThreeBBAseemblyRequest(BaseModel):
    building_block_1: AssemblyLeafNodeInputs
    building_block_2: AssemblyLeafNodeInputs
    intermediate_product_1: ReactionNodeInputs
    building_block_3: AssemblyLeafNodeInputs
    product: ReactionNodeInputs
    unmapped_inputs: Optional[list[AssemblyInputItem]]

class CustomAssemblySchema(BaseModel):
    assembly_schema: dict
    mapped_inputs: Optional[dict[str, list[AssemblyInputItem]]]
    unmapped_inputs: Optional[list[AssemblyInputItem]]
    
