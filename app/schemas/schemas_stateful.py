from typing import Union, Optional
from pydantic import BaseModel
from beanie import Document

from .schemas_common import TemplateConfig, TemplateEvalResponse
from .schemas_assembly import AssemblyInputItem, TwoBBAseemblyRequest, ThreeBBAseemblyRequest, CustomAssemblySchema

class TemplateDocument(Document):
    template_config: TemplateConfig

class EvalRequestStateful(BaseModel):
    inputs: list[str]

class AssemblyLeafNodeInputsStateful(BaseModel):
    inputs: list[AssemblyInputItem]
    template_config: Optional[TemplateConfig]
    template_id: Optional[str]

class ReactionNodeInputsStateful(BaseModel):
    reaction_mechanisms: dict[str, bool]
    template_config: Optional[TemplateConfig]
    template_id: Optional[str]

class TwoBBAseemblyRequestStateful(BaseModel):
    building_block_1: AssemblyLeafNodeInputsStateful
    building_block_2: AssemblyLeafNodeInputsStateful
    product: ReactionNodeInputsStateful
    unmapped_inputs: Optional[list[AssemblyInputItem]]

class ThreeBBAseemblyRequestStateful(BaseModel):
    building_block_1: AssemblyLeafNodeInputsStateful
    building_block_2: AssemblyLeafNodeInputsStateful
    intermediate_product_1: ReactionNodeInputsStateful
    building_block_3: AssemblyLeafNodeInputsStateful
    product: ReactionNodeInputsStateful
    unmapped_inputs: Optional[list[AssemblyInputItem]]

class CreateAssemblySchema(BaseModel):
    assembly_schema: dict

class AssemblySchemaDocument(Document):
    assembly_schema: dict

class CustomAssemblySchemaStateful(BaseModel):
    assembly_schema: Optional[dict]
    assembly_schema_id: Optional[str]
    mapped_inputs: Optional[dict[str, list[AssemblyInputItem]]]
    unmapped_inputs: Optional[list[AssemblyInputItem]]
    

