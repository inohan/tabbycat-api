from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .enums import PermissionsEnum

@dataclass
class Group(BaseModel):
    id: str = None
    url: str = None
    name: str = None
    permissions: list[PermissionsEnum] = None
    users: list[int] = None
    
    FIELDS_REQUIRED = ["id", "url", "name", "users"]
    FIELDS_READONLY = ["id", "url", "users"]
    FIELDS_URL_STR = ["url"]

@dataclass
class PaginatedGroups(PaginatedModel[Group]):
    pass