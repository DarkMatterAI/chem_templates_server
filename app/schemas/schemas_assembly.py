from typing import Union, Optional
from pydantic import BaseModel

from .schemas_common import TemplateConfig

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

class ThreeBBAseemblyRequest(BaseModel):
    building_block_1: AssemblyLeafNodeInputs
    building_block_2: AssemblyLeafNodeInputs
    intermediate_product_1: ReactionNodeInputs
    building_block_3: AssemblyLeafNodeInputs
    product: ReactionNodeInputs

class CustomAssemblySchema(BaseModel):
    assembly_schema: dict 
    input_schema: dict[str, list[AssemblyInputItem]]
    


# class SynthonNodeSchema(BaseModel):
#     name: str 
#     node_type: str 
#     n_func: list[int]
#     template_config: Optional[TemplateConfig]
#     reaction_mechanisms: dict[str, bool]
#     incoming_node: type(None)
#     next_node: type(None)

# class SynthonLeafNodeSchema(BaseModel):
#     name: str 
#     node_type: str 
#     n_func: list[int]
#     template_config: Optional[TemplateConfig]

# class FragmentNodeSchema(BaseModel):
#     name: str
#     node_type: str 
#     template_config: Optional[TemplateConfig]
#     children: list 

# class FragmentLeafNodeSchema(BaseModel):
#     name: str
#     node_type: str 
#     mapping_idxs: list[int]
#     template_config: Optional[TemplateConfig]

# class NodeSchemaData(BaseModel):
#     synthon_node: SynthonNodeSchema
#     synthon_leaf_node: SynthonLeafNodeSchema
#     fragment_node: FragmentNodeSchema
#     fragment_leaf_node: FragmentLeafNodeSchema






# class BBAssemblySchema(BaseModel):
#     template_config: TemplateConfig

# class ProductAssemblySchema(BaseModel):
#     reaction_mechanisms: dict[str, bool]
#     template_config: TemplateConfig 

# class AssemblySchema2BB(BaseModel):
#     building_block_1: BBAssemblySchema
#     building_block_2: BBAssemblySchema
#     product: ProductAssemblySchema

# class AssemblySchema3BB(BaseModel):
#     building_block_1: BBAssemblySchema
#     building_block_2: BBAssemblySchema
#     intermediate_product_1: ProductAssemblySchema
#     building_block_3: BBAssemblySchema
#     product: ProductAssemblySchema


# class AssemblyInputs2BB(BaseModel):
#     building_block_1_inputs: list[str]
#     building_block_2_inputs: list[str]

# class AssemblyInputs3BB(AssemblyInputs2BB):
#     building_block_3_inputs: list[str]


# class AssemblyRequest2BB(BaseModel):
#     assembly_schema: AssemblySchema2BB
#     assembly_inputs: AssemblyInputs2BB

# class AssemblyRequest3BB(BaseModel):
#     assembly_schema: AssemblySchema3BB
#     assembly_inputs: AssemblyInputs3BB
