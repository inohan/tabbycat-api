import dataclasses

from .venue_category import VenueCategory
from .base_model import BaseModel

@dataclasses.dataclass
class VenueConstraint(BaseModel):
    category:VenueCategory = None
    priority:int = None

    FIELDS_REQUIRED = ["category", "priority"]
    FIELDS_READONLY = []
    FIELDS_URL_STR = ["category"]
    FIELDS_URL_LIST = []
