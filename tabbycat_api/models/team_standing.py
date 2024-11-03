from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .team import Team
from .enums import TeamStandingsMetricEnum

@dataclass
class TeamStandingMetric(BaseModel):
    metric: TeamStandingsMetricEnum = None
    value: float|int = None

@dataclass
class TeamStanding(BaseModel):
    rank: int = None
    tied: bool = None
    metrics: list[TeamStandingMetric] = None
    team: Team = None
    
    FIELDS_REQUIRED = ["rank", "tied", "metrics", "team"]
    FIELDS_READONLY = ["rank", "tied", "team"]
    FIELDS_URL_STR = ["team"]

@dataclass
class PaginatedTeamStandings(PaginatedModel[TeamStanding]):
    async def fetch(self, category: int = None, round: int = None, metrics: list[TeamStandingsMetricEnum] = None, extra_metrics: list[TeamStandingsMetricEnum] = None):
        await super().fetch(params={"category": category, "round": round, "metrics": metrics, "extra_metrics": extra_metrics})