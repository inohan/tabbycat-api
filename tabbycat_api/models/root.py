from dataclasses import dataclass
from .base_model import BaseModel

from .v1root import V1Root

@dataclass
class RootLinks(BaseModel):
    v1: V1Root = None
    
    FIELDS_REQUIRED = ["v1"]
    FIELDS_READONLY = ["v1"]
    FIELDS_URL_STR = ["v1"]

@dataclass
class Root(BaseModel):
    _links: RootLinks = None
    timezone: str = None
    version: str = None
    
    FIELDS_REQUIRED = ["_links", "timezone", "version"]
    FIELDS_READONLY = ["_links", "timezone"]