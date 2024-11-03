from dataclasses import dataclass
from .base_model import BaseModel

from .team import Team

@dataclass
class BreakEligibility(BaseModel):
    slug: str = None
    team_set: list[Team] = None
    url: str = None
    
    FIELDS_REQUIRED = ["slug", "team_set"]
    FIELDS_READONLY = ["slug", "url"]
    FIELDS_URL_STR = ["url"]
    FIELDS_URL_LIST = ["team_set"]