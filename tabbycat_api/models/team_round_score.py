from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .team import Team
from .round import Round

@dataclass
class Score(BaseModel):
    round: Round = None
    points: int = None
    score: float|int = None
    has_ghost: bool = None
    
    FIELDS_REQUIRED = ["round", "points", "score", "has_ghost"]
    FIELDS_URL_STR = ["round"]

@dataclass
class TeamRoundScore(BaseModel):
    team: Team = None
    rounds: list[Score] = None
    
    FIELDS_REQUIRED = ["team", "rounds"]
    FIELDS_READONLY = ["team"]
    FIELDS_URL_STR = ["team"]

@dataclass
class PaginatedTeamRoundScores(PaginatedModel[TeamRoundScore]):
    pass