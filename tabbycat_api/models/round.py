from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .enums import RoundStageEnum, RoundDrawTypeEnum, RoundDrawStatusEnum
from .availability import PaginatedAvailabilities
from .preformed_panel import PaginatedPreformedPanels
from .round_pairing import PaginatedRoundPairings
from .break_category import BreakCategory
from .round_motion import RoundMotion

@dataclass
class RoundLinks(BaseModel):
    pairing: PaginatedRoundPairings = None
    availabilities: PaginatedAvailabilities = None
    preformed_panels: PaginatedPreformedPanels = None
    
    FIELDS_REQUIRED = ["pairing", "availabilities", "preformed_panels"]
    FIELDS_READONLY = ["pairing", "availabilities", "preformed_panels"]
    FIELDS_URL_STR = ["pairing", "availabilities", "preformed_panels"]

@dataclass
class Round(BaseModel):
    id: int = None
    url: str = None
    break_category: BreakCategory = None
    motions: list[RoundMotion] = None
    starts_at: str = None
    _links: RoundLinks = None
    seq: int = None
    completed: bool = None
    name: str = None
    abbreviation: str = None
    stage: RoundStageEnum = None
    draw_type: RoundDrawTypeEnum = None
    draw_status:RoundDrawStatusEnum = None
    feedback_weight: float|int = None
    silent: bool = None
    motions_released: bool = None
    weight: float|int = None
    
    FIELDS_REQUIRED = ["id", "url", "_links", "seq", "name", "abbreviation", "draw_type"]
    FIELDS_READONLY = ["id", "url", "_links"]
    FIELDS_URL_STR = ["url", "break_category"]

@dataclass
class PaginatedRounds(PaginatedModel[Round]):
    pass