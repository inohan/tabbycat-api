from dataclasses import dataclass, field
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .checkin import Checkin
from .speaker_category import SpeakerCategory

@dataclass
class SpeakerLinks(BaseModel):
    checkin: Checkin = None
    
    FIELDS_REQUIRED = ["checkin"]
    FIELDS_READONLY = ["checkin"]
    FIELDS_URL_STR = ["checkin"]

@dataclass
class Speaker(BaseModel):
    id: int = None
    url: str = None
    name: str = None
    team: "Team" = None
    categories: list[SpeakerCategory] = field(default=None, repr=False)
    _links: SpeakerLinks = field(default=None, repr=False)
    barcode: str = field(default=None, repr=False)
    email: str = field(default=None, repr=False)
    phone: str = field(default=None, repr=False)
    anonymous: bool = field(default=None, repr=False)
    code_name: str = field(default=None, repr=False)
    url_key: str = field(default=None, repr=False)
    gender: str = field(default=None, repr=False)
    pronoun: str = field(default=None, repr=False)
    
    FIELDS_REQUIRED = ["id", "url", "name", "team", "categories", "_links", "barcode"]
    FIELDS_READONLY = ["id", "url", "_links", "barcode"]
    FIELDS_URL_STR = ["url", "team"]
    FIELDS_URL_LIST = ["categories"]
    __hash__ = BaseModel.__hash__

@dataclass
class PaginatedSpeakers(PaginatedModel[Speaker]):
    pass

from .team import Team