from typing import Union, Optional
from pydantic import BaseModel
from beanie import Document

from .schemas_common import (
                            FilterRange, 
                            IncludeCatalog, 
                            SmartsFilters, 
                            TemplateConfig,
                            TemplateEvalResponse
                            )

class TemplateDocument(Document):
    template_config: TemplateConfig

class EvalRequestStateful(BaseModel):
    queries: list[str]
