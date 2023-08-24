from typing import Union, Optional
from pydantic import BaseModel

class FilterRange(BaseModel):
    min_val: Optional[Union[float, int]]
    max_val: Optional[Union[float, int]]

class IncludeCatalog(BaseModel):
    include: bool

class SmartsFilters(BaseModel):
    property_filters: dict[str, FilterRange]

class TemplateConfig(BaseModel):
    template_name: Optional[str]
    property_filters: dict[str, FilterRange]
    catalog_filters: dict[str, IncludeCatalog]
    smarts_filters: dict[str, FilterRange]


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

class TemplateResponseData(BaseModel):
    template_name: Optional[str]
    valid_input: bool
    property_filters: dict[str, PropertyResult]
    catalog_filters: dict[str, CatalogResult]
    smarts_filters: dict[str, SmartsResult]

class TemplateEvalResponse(BaseModel):
    input: str 
    result: bool
    template_data: Optional[TemplateResponseData]
    

