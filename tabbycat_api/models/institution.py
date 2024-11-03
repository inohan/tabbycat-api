from dataclasses import dataclass, field
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .venue_constraints import VenueConstraint


@dataclass
class Institution(BaseModel):
    id: int = None
    url: str = None
    region:str = field(default=None, repr=False)
    venue_constraints:list[VenueConstraint] = field(default=None, repr=False)
    name:str = None
    code:str = None

    FIELDS_READONLY = ["id", "url"]
    FIELDS_REQUIRED = ["id", "url", "name", "code"]
    FIELDS_URL_STR = ["url"]

@dataclass
class PaginatedInstitutions(PaginatedModel[Institution]):
    pass