from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .round import Round

@dataclass
class MotionRound(BaseModel):
    round: Round = None
    seq: int = None
    
    FIELDS_REQUIRED = ["round"]
    FIELDS_URL_STR= ["round"]

@dataclass
class Motion(BaseModel):
    id: int = None
    url: str = None
    rounds: list[MotionRound] = None
    info_slide_plain: str = None
    text: str = None
    reference: str = None
    info_slide: str = None
    
    FIELDS_REQUIRED = ["id", "url", "rounds", "info_slide_plain", "text", "reference"]
    FIELDS_READONLY = ["id", "url", "info_slide_plain"]
    FIELDS_URL_STR = ["url"]

@dataclass
class PaginatedMotions(PaginatedModel[Motion]):
    pass