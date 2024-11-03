from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .enums import PreformedPanelImportanceEnum
from .debate import DebateAdjudicator

@dataclass
class PreformedPanel(BaseModel):
    id: int = None
    url: str = None
    adjudicators: DebateAdjudicator = None
    importance: PreformedPanelImportanceEnum = None
    bracket_min: float|int = None
    bracket_max: float|int = None
    room_rank: int = None
    liveness: int = None
    
    FIELDS_REQUIRED = ["id", "url"]
    FIELDS_READONLY = ["id", "url"]
    FIELDS_URL_STR = ["url"]

@dataclass
class PaginatedPreformedPanels(PaginatedModel[PreformedPanel]):
    pass