from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .speaker import Speaker
from .enums import SpeakerStandingsMetricEnum

@dataclass
class SpeakerStandingMetric(BaseModel):
    metric: SpeakerStandingsMetricEnum = None
    value: float|int = None

@dataclass
class SpeakerStanding(BaseModel):
    rank: int = None
    tied: bool = None
    metrics: list[SpeakerStandingMetric] = None
    speaker: Speaker = None
    
    FIELDS_REQUIRED = ["rank", "tied", "metrics", "speaker"]
    FIELDS_READONLY = ["rank", "tied", "metrics"]
    FIELDS_URL_STR = ["speaker"]

@dataclass
class PaginatedSpeakerStandings(PaginatedModel[SpeakerStanding]):
    async def fetch(self, category: int = None, round: int = None, metrics: list[SpeakerStandingsMetricEnum] = None, extra_metrics: list[SpeakerStandingsMetricEnum] = None):
        await super().fetch(params={"category": category, "round": round, "metrics": metrics, "extra_metrics": extra_metrics})