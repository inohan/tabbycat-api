from dataclasses import dataclass, field
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .enums import EmojiEnum, BlankEnum, GenderEnum
from .break_category import BreakCategory
from .institution import Institution
from .venue_constraints import VenueConstraint

@dataclass
class TeamSpeaker(BaseModel):
    id: int = field(default=None, repr=False)
    url: str = None
    name: str = None
    categories: list["SpeakerCategory"] = field(default=None, repr=False)
    _links: "SpeakerLinks" = field(default=None, repr=False)
    barcode: str = field(default=None, repr=False)
    email: str = field(default=None, repr=False)
    phone: str = field(default=None, repr=False)
    anonymous: bool = field(default=None, repr=False)
    code_name: str = field(default=None, repr=False)
    url_key: str = field(default=None, repr=False)
    gender: GenderEnum = field(default=None, repr=False)
    pronoun: str = field(default=None, repr=False)
    
    FIELDS_REQUIRED = ["id", "url", "name", "categories", "_links", "barcode"]
    FIELDS_READONLY = ["id", "url", "_links", "barcode"]
    FIELDS_URL_STR = ["url"]
    FIELDS_URL_LIST = ["categories"]
    
    async def fetch(self):
        raise AttributeError("TeamSpeaker object does not have a fetch method")

@dataclass
class Team(BaseModel):
    id: int = None
    url: str = None
    institution: Institution = field(default=None, repr=False)
    break_categories: list[BreakCategory] = field(default=None, repr=False)
    institution_conflicts: list[Institution] = field(default=None, repr=False)
    venue_constraints: list[VenueConstraint] = field(default=None, repr=False)
    reference: str = None
    short_reference: str = field(default=None, repr=False)
    code_name: str = None
    short_name: str = field(default=None, repr=False)
    long_name: str = field(default=None, repr=False)
    use_institution_prefix: bool = field(default=None, repr=False)
    seed: int = field(default=None, repr=False)
    emoji: EmojiEnum | BlankEnum = None
    speakers: list[TeamSpeaker] = None
    
    FIELDS_REQUIRED = ["id", "url", "short_name", "long_name"]
    FIELDS_READONLY = ["id", "url", "short_name", "long_name"]
    FIELDS_URL_STR = ["url", "institution"]
    FIELDS_URL_LIST = ["break_categories", "institution_conflicts", "venue_constraints"]
    __hash__ = BaseModel.__hash__

@dataclass
class PaginatedTeams(PaginatedModel[Team]):
    pass

from .speaker_category import SpeakerCategory
from .speaker import SpeakerLinks