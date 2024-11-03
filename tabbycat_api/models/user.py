from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .enums import PermissionsEnum
from .tournament import Tournament
from .group import Group

@dataclass
class TournamentPermissions(BaseModel):
    tournament: Tournament = None
    groups: list[Group] = None
    permissions: list[PermissionsEnum] = None
    
    FIELDS_REQUIRED = ["tournament"]
    FIELDS_READONLY = ["tournament"]
    FIELDS_URL_STR = ["tournament"]
    FIELDS_URL_LIST = ["groups"]

@dataclass
class User(BaseModel):
    id: int = None
    url: str = None
    username: str = None
    password: str = None
    is_superuser: bool = None
    is_staff: bool = None
    email: str = None
    is_active: bool = None
    date_joined: str = None
    last_login: str = None
    tournaments: list[TournamentPermissions] = None
    
    FIELDS_REQUIRED = ["id", "url", "username", "password", "date_joined", "last_login"]
    FIELDS_READONLY = ["id", "url", "date_joined", "last_login"]
    FIELDS_URL_STR = ["url"]

@dataclass
class PaginatedUsers(PaginatedModel[User]):
    pass