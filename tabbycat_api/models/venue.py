from dataclasses import dataclass, field
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .checkin import Checkin
from .venue_category import VenueCategory

@dataclass
class VenueLinks(BaseModel):
    checkin: Checkin = None
    
    FIELDS_REQUIRED = ["checkin"]
    FIELDS_READONLY = ["checkin"]
    FIELDS_URL_STR = ["checkin"]

@dataclass
class Venue(BaseModel):
    id: int = None
    url: str = None
    categories: list[VenueCategory] = field(default=None, repr=False)
    display_name: str = None
    external_url: str = field(default=None, repr=False)
    _links: str = field(default=None, repr=False)
    name: str = None
    priority: int = field(default=None, repr=False)
    
    FIELDS_REQUIRED = ["id", "url", "categories", "display_name", "_links", "name", "priority"]
    FIELDS_READONLY = ["id", "url", "display_name", "_links"]
    FIELDS_URL_STR = ["url"]
    FIELDS_URL_LIST = ["categories"]

@dataclass
class PaginatedVenues(PaginatedModel[Venue]):
    pass