from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .speaker import Speaker
from .round import Round

@dataclass
class RoundSpeech(BaseModel):
    score: float|int = None
    position: int = None
    ghost: bool = None
    
    FIELDS_REQUIRED = ["score", "position"]

@dataclass
class RoundScores(BaseModel):
    round: Round = None
    speeches: list[RoundSpeech] = None
    
    FIELDS_REQUIRED = ["round", "speeches"]
    FIELDS_URL_STR = ["round"]

@dataclass
class SpeakerRoundScore(BaseModel):
    speaker: Speaker = None
    rounds: list[RoundScores] = None
    
    FIELDS_REQUIRED = ["speaker", "rounds"]
    FIELDS_READONLY = ["speaker"]
    FIELDS_URL_STR = ["speaker"]

@dataclass
class PaginatedSpeakerRoundScores(PaginatedModel[SpeakerRoundScore]):
    async def fetch(self, substantive: bool = None, replies: bool = None, ghost: bool = None):
        return await super().fetch(params={"substantive": substantive, "replies": replies, "ghost": ghost})        