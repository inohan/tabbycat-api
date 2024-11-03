from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .enums import RemarkEnum, BlankEnum
from .team import Team

@dataclass
class BreakingTeam(BaseModel):
    team: Team = None
    rank: int = None
    break_rank: int = None
    remark: RemarkEnum | BlankEnum = None
    
    FIELDS_REQUIRED = ["team", "rank"]
    FIELDS_URL_STR = ["team"]

class PaginatedBreakingTeams(PaginatedModel[BreakingTeam]):
    pass