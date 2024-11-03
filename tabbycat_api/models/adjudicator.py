from dataclasses import dataclass, field

from .checkin import Checkin
from .institution import Institution
from .team import Team
from .venue_constraints import VenueConstraint
from .enums import BlankEnum, GenderEnum
from .base_model import BaseModel
from .paginated_model import PaginatedModel

@dataclass
class AdjudicatorLinks(BaseModel):
    checkin: Checkin = None
    
    FIELDS_REQUIRED = ["checkin"]
    FIELDS_READONLY = ["checkin"]
    FIELDS_URL_STR = ["checkin"]

@dataclass
class Adjudicator(BaseModel):
    id: int = None
    url: str = None
    name: str = None
    institution: Institution = field(default=None, repr=False)
    institution_conflicts: list[Institution] = field(default=None, repr=False)
    team_conflicts: list[Team] = field(default=None, repr=False)
    adjudicator_conflicts: list["Adjudicator"] = field(default=None, repr=False)
    venue_constraints: list[VenueConstraint] = field(default=None, repr=False)
    _links: AdjudicatorLinks = field(default=None, repr=False)
    barcode: str = field(default=None, repr=False)
    email: str = field(default=None, repr=False)
    phone: str = field(default=None, repr=False)
    anonymous: bool = field(default=None, repr=False)
    code_name: str = field(default=None, repr=False)
    url_key: str = field(default=None, repr=False)
    gender: GenderEnum|BlankEnum = field(default=None, repr=False)
    pronoun: str = field(default=None, repr=False)
    base_score: float = field(default=None, repr=False)
    trainee: bool = field(default=None, repr=False)
    breaking: bool = field(default=None, repr=False)
    independent: bool = field(default=None, repr=False)
    adj_core: bool = field(default=None, repr=False)

    FIELDS_READONLY = ["client", "id", "url", "_links", "barcode"]
    FIELDS_REQUIRED = ["name", "institution", "institution_conflicts", "team_conflicts", "id", "url", "_links", "barcode"]
    FIELDS_URL_STR = ["url", "institution"]
    FIELDS_URL_LIST = ["institution_conflicts", "team_conflicts", "adjudicator_conflicts"]
    __hash__ = BaseModel.__hash__

@dataclass
class PaginatedAdjudicators(PaginatedModel[Adjudicator]):
    pass