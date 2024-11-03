from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .enums import AnswerTypeEnum

@dataclass
class FeedbackQuestion(BaseModel):
    id: int = None
    url: str = None
    seq: int = None
    text: str = None
    name: str = None
    reference: str = None
    from_adj: bool = None
    from_team: bool = None
    answer_type: AnswerTypeEnum = None
    required: bool = None
    min_value: float|int = None
    max_value: float|int = None
    choices: list[str] = None
    
    FIELDS_REQUIRED = ["id", "url", "seq", "text", "name", "reference", "from_adj", "from_team", "answer_type"]
    FIELDS_READONLY = ["id", "url"]
    FIELDS_URL_STR = ["url"]

@dataclass
class PaginatedFeedbackQuestions(PaginatedModel[FeedbackQuestion]):
    pass