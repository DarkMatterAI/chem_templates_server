from typing import Union, Optional
from pydantic import BaseModel
from beanie import Document

from .schemas_common import TemplateConfig, TemplateEvalResponse
from .schemas_assembly import (
                                TwoBBAseemblyRequest, 
                                ThreeBBAseemblyRequest, 
                                CustomAssemblySchema,
                                )

class TemplateDocument(Document):
    template_config: TemplateConfig

class EvalRequestStateful(BaseModel):
    inputs: list[str]

