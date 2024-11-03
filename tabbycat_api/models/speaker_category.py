from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel


@dataclass
class SpeakerCategoryLinks(BaseModel):
    eligibility: "SpeakerEligibility" = None
    
    FIELDS_REQUIRED = ["eligibility"]
    FIELDS_READONLY = ["eligibility"]
    FIELDS_URL_STR = ["eligibility"]

@dataclass
class SpeakerCategory(BaseModel):
    id: int = None
    url: str = None
    _links: SpeakerCategoryLinks = None
    name: str = None
    slug: str = None
    seq: int = None
    limit: int = None
    public: bool = None
    
    FIELDS_REQUIRED = ["id", "url", "_links", "name", "slug", "seq"]
    FIELDS_READONLY = ["id", "url", "_links"]
    FIELDS_URL_STR = ["url"]

@dataclass
class PaginatedSpeakerCategories(PaginatedModel[SpeakerCategory]):
    pass

from .speaker_eligibility import SpeakerEligibility