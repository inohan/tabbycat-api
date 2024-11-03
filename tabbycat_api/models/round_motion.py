from dataclasses import dataclass
from .base_model import BaseModel

@dataclass
class RoundMotion(BaseModel):
    id: int = None
    url: str = None
    text: str = None
    reference: str = None
    info_slide: str = None
    info_slide_plain: str = None
    seq: int = None
    
    FIELDS_READONLY = ["id", "info_slide_plain", "seq"]
    FIELDS_REQUIRED = ["id", "info_slide_plain", "seq"]
    FIELDS_URL_STR = ["url"]