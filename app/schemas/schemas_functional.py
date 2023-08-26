from typing import Union, Optional
from pydantic import BaseModel
from .schemas_common import (
                            FilterRange, 
                            IncludeCatalog, 
                            SmartsFilters, 
                            TemplateConfig,
                            TemplateEvalResponse
                            )

class TemplateEvalRequestFunctional(BaseModel):
    inputs: list[str]
    template_config: TemplateConfig
