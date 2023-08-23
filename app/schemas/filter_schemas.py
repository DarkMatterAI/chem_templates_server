from typing import Union, Optional

from pydantic import BaseModel

class ComputePropertiesRequest(BaseModel):
    queries: list[str]
    property_names: Optional[list[str]]

class ComputePropertiesResponse(BaseModel):
    results: list[dict]

class ComputeCatalogRequest(BaseModel):
    queries: list[str]
    catalog_names: Optional[list[str]]

class ComputeCatalogResponse(BaseModel):
    results: list[dict]



class FilterRange(BaseModel):
    min_val: Optional[Union[float, int]]
    max_val: Optional[Union[float, int]]

class IncludeCatalog(BaseModel):
    include: bool

class SmartsFilters(BaseModel):
    property_filters: dict[str, FilterRange]

class TemplateConfig(BaseModel):
    property_filters: dict[str, FilterRange]
    catalog_filters: dict[str, IncludeCatalog]
    smarts_filters: dict[str, FilterRange]



class TemplateEvalRequest(BaseModel):
    queries: list[str]
    template_config: TemplateConfig

class PropertyResult(BaseModel):
    min_val: Optional[Union[float, int]]
    max_val: Optional[Union[float, int]]
    value: Optional[Union[float, int]]
    result: bool 

class CatalogResult(BaseModel):
    include: bool
    has_match: bool
    result: bool

class SmartsResult(BaseModel):
    num_matches: Optional[int]
    min_val: Optional[Union[float, int]]
    max_val: Optional[Union[float, int]]
    result: bool 

class TemplateEvalResponse(BaseModel):
    input: str
    result: bool

class TemplateEvalResponseVerbose(TemplateEvalResponse):
    valid_input: bool
    property_filters: dict[str, PropertyResult]
    catalog_filters: dict[str, CatalogResult]
    smarts_filters: dict[str, SmartsResult]

