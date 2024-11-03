from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .enums import VenueCategoryDisplayEnum

@dataclass
class VenueCategory(BaseModel):
    id: int = None
    url: str = None
    venues: list["Venue"] = None
    name: str = None
    description: str = None
    display_in_venue_name: VenueCategoryDisplayEnum = None
    display_in_public_tooltip: bool = None

    FIELDS_REQUIRED = ["id", "url", "venues", "name"]
    FIELDS_READONLY = ["id", "url"]
    FIELDS_URL_STR = ["url"]
    FIELDS_URL_LIST = ["venues"]

@dataclass
class PaginatedVenueCategories(PaginatedModel[VenueCategory]):
    pass

from .venue import Venue