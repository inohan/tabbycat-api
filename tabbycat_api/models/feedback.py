from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel
from typing import Literal

from .enums import SubmitterTypeEnum
from .feedback_question import FeedbackQuestion
from .adjudicator import Adjudicator
from .team import Team
from .speaker import Speaker
from .round_pairing import RoundPairing

@dataclass
class FeedbackAnswer(BaseModel):
    question: FeedbackQuestion = None
    answer: str|float|int|bool = None
    
    FIELDS_REQUIRED = ["question", "answer"]
    FIELDS_URL_STR = ["question"]

@dataclass
class Feedback(BaseModel):
    id: int = None
    url: str = None
    adjudicator: Adjudicator = None
    source: Adjudicator|Team = None
    participant_submitter: Adjudicator|Speaker = None
    debate: RoundPairing = None
    answers: list[FeedbackAnswer] = None
    timestamp: str = None
    version: int = None
    submitter_type: SubmitterTypeEnum = None
    confirmed: bool = None
    private_url: bool = None
    confirm_timestamp: str = None
    ip_address: str = None
    score: float|int = None
    ignored: bool = None
    submitter: int = None
    confirmer: int = None
    
    FIELDS_REQUIRED = ["id", "url", "adjudicator", "source", "participant_submitter", "debate", "timestamp", "version", "submitter_type", "private_url", "confirm_timestamp", "ip_address", "score", "submitter", "confirmer"]
    FIELDS_READONLY = ["id", "url", "timestamp", "version", "submitter_type", "private_url", "confirm_timestamp", "ip_address", "submitter", "confirmer"]
    FIELDS_URL_STR = ["url", "adjudicator", "source", "participant_submitter", "debate"]

@dataclass
class PaginatedFeedbacks(PaginatedModel[Feedback]):
    async def fetch(self, round: list[int] = None, source_type: Literal["adjudicator", "team"] = None, source: int = None, target: int = None, **kwargs):
        return await super().fetch(params={"round": round, "source_type": source_type, "source": source, "target": target})