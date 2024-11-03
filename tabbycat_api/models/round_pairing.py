from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .enums import ResultStatusEnum
from .debate import DebateAdjudicator, DebateTeam
from .venue import Venue

@dataclass
class PairingLinks(BaseModel):
    ballots: "PaginatedBallots" = None
    
    FIELDS_REQUIRED = ["ballots"]
    FIELDS_READONLY = ["ballots"]
    FIELDS_URL_STR = ["ballots"]

@dataclass
class RoundPairing(BaseModel):
    id: int = None
    url: str = None
    venue: Venue = None
    teams: list[DebateTeam] = None
    adjudicators: DebateAdjudicator = None
    _links: PairingLinks = None
    bracket: float|int = None
    room_rank: int = None
    importance: int = None
    result_status: ResultStatusEnum = None
    sides_confirmed: bool = None
    
    FIELDS_REQUIRED = ["id", "url", "teams", "_links"]
    FIELDS_READONLY = ["id", "url", "_links"]
    FIELDS_URL_STR = ["url", "venue"]

@dataclass
class PaginatedRoundPairings(PaginatedModel[RoundPairing]):
    pass

from .ballot import PaginatedBallots