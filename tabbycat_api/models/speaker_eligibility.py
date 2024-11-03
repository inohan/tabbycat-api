from dataclasses import dataclass
from .base_model import BaseModel


@dataclass
class SpeakerEligibility(BaseModel):
    url: str = None
    slug: str = None
    speaker_set: list["Speaker"] = None
    
    FIELDS_REQUIRED = ["slug", "speaker_set"]
    FIELDS_READONLY = ["url", "slug"]
    FIELDS_URL_STRING = ["url"]
    FIELDS_URL_LIST = ["speaker_set"]

    from .speaker import Speaker