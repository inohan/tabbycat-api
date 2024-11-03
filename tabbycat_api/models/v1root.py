from dataclasses import dataclass
from .base_model import BaseModel

from .institution import PaginatedInstitutions
from .tournament import PaginatedTournaments
from .user import PaginatedUsers

@dataclass
class V1Links(BaseModel):
    tournaments: PaginatedTournaments = None
    institutions: PaginatedInstitutions = None
    users: PaginatedUsers = None
    
    FIELDS_REQUIRED = ["tournaments", "institutions", "users"]
    FIELDS_READONLY = ["tournaments", "institutions", "users"]
    FIELDS_URL_STR = ["tournaments", "institutions", "users"]

@dataclass
class V1Root(BaseModel):
    _links: V1Links = None
    
    FIELDS_REQUIRED = ["_links"]
    FIELDS_READONLY = ["_links"]