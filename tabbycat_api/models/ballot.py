from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .enums import SubmitterTypeEnum, SideEnum
from .adjudicator import Adjudicator
from .team import Team
from .speaker import Speaker
from .motion import Motion

@dataclass
class Criteria(BaseModel):
    criterion: BaseModel = None
    score: float|int = None
    
    FIELDS_REQUIRED = ["criterion", "score"]
    FIELDS_URL_STR = ["criterion"]

@dataclass
class Speech(BaseModel):
    ghost: bool = None
    score: float|int = None
    rank: int = None
    speaker: Speaker = None
    criteria: Criteria = None
    
    FIELDS_REQUIRED = ["score", "speaker"]
    FIELDS_URL_STR = ["speaker"]

@dataclass
class TeamResult(BaseModel):
    side: int | SideEnum = None
    points: int = None
    win: bool = None
    score: float|int = None
    team: Team = None
    speeches: list[Speech] = None
    
    FIELDS_REQUIRED = ["team"]
    FIELDS_URL_STR = ["team"]

@dataclass
class Sheet(BaseModel):
    teams: list[TeamResult] = None
    adjudicator: Adjudicator = None
    
    FIELDS_REQUIRED = ["teams"]
    FIELDS_URL_STR = ["adjudicator"]

@dataclass
class Result(BaseModel):
    sheets: list[Sheet] = None
    
    FIELDS_REQUIRED = ["sheets"]

@dataclass
class Veto(BaseModel):
    team: Team = None
    motion: Motion = None
    
    FIELDS_REQUIRED = ["team", "motion"]
    FIELDS_URL_STR = ["team", "motion"]

@dataclass
class Ballot(BaseModel):
    id: int = None
    result: Result = None
    motion: Motion = None
    url: str = None
    participant_submitter: Adjudicator = None
    vetos: list[Veto] = None
    timestamp: str = None
    version: int = None
    submitter_type: SubmitterTypeEnum = None
    confirmed: bool = None
    private_url: bool = None
    confirm_timestamp: str = None
    ip_address: str = None
    discarded: bool = None
    single_adj: bool = None
    submitter: int = None
    confirmer: int = None
    
    FIELDS_REQUIRED = ["id", "result", "url", "timestamp", "version", "submitter_type", "private_url", "confirm_timestamp", "ip_address", "submitter", "confirmer"]
    FIELDS_READONLY = ["id", "url", "timestamp", "version", "submitter_type", "private_url", "confirm_timestamp", "ip_address", "submitter", "confirmer"]
    FIELDS_URL_STR = ["motion", "url", "participant_submitter"]

class PaginatedBallots(PaginatedModel[Ballot]):
    async def fetch(self, confirmed: bool = None):
        await super().fetch(params={"confirmed": confirmed})