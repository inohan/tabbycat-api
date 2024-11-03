from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .enums import BreakCategoryRuleEnum


@dataclass
class BreakCategoryLinks(BaseModel):
    eligibility: "BreakEligibility" = None
    breaking_teams: "PaginatedBreakingTeams" = None
    
    FIELDS_REQUIRED = ["eligibility", "breaking_teams"]
    FIELDS_READONLY = ["eligibility", "breaking_teams"]
    FIELDS_URL_STR = ["eligibility", "breaking_teams"]

@dataclass
class BreakCategory(BaseModel):
    id: int = None
    url: str = None
    _links: BreakCategoryLinks = None
    name: str = None
    slug: str = None
    seq: int = None
    break_size: int = None
    is_general: bool = None
    priority: int = None
    limit: int = None
    rule: BreakCategoryRuleEnum = None
    
    FIELDS_REQUIRED = ["id", "url", "_links", "name", "slug", "seq", "break_size", "is_general", "priority"]
    FIELDS_READONLY = ["id", "url", "_links"]
    FIELDS_URL_STR = ["url"]

@dataclass
class PaginatedBreakCategories(PaginatedModel[BreakCategory]):
    pass

from .break_eligibility import BreakEligibility
from .breaking_team import PaginatedBreakingTeams