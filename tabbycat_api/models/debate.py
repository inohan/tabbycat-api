from dataclasses import dataclass
from .base_model import BaseModel

from .enums import SideEnum
from .adjudicator import Adjudicator
from .team import Team

@dataclass
class DebateAdjudicator(BaseModel):
    chair: Adjudicator = None
    panellists: list[Adjudicator] = None
    trainees: list[Adjudicator] = None
    
    FIELDS_REQUIRED = ["chair", "panelists", "trainees"]
    FIELDS_URL_STR = ["chair"]
    FIELDS_URL_LIST = ["panelists", "trainees"]

@dataclass
class DebateTeam(BaseModel):
    team: Team = None
    side: int|SideEnum = None
    
    FIELDS_REQUIRED = ["team"]
    FIELDS_URL_STR = ["team"]