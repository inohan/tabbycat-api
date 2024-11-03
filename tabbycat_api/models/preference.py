from typing import Any

from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

@dataclass
class Preference(BaseModel):
    section: str = None
    name: str = None
    identifier: str = None
    default: Any = None
    value: Any = None
    verbose_name: str = None
    help_text: str = None
    additional_data: Any = None
    field: Any = None
    url: str = None # Manually initialized
    
    FIELDS_REQUIRED = ["section", "name", "identifier", "default", "value", "verbose_name", "help_text", "additional_data", "field"]
    FIELDS_READONLY = ["url", "section", "name", "identifier", "default", "verbose_name", "help_text", "additional_data", "field"]
    FIELDS_URL_STR = ["url"]
    
    def update(self, **kwargs) -> None:
        super().update(**kwargs)
        if self.client and self.identifier:
            self.url = f"/api/v1/tournaments/{self.client.tournament_slug}/preferences/{self.identifier}"

@dataclass
class PaginatedPreferences(PaginatedModel[Preference]):
    pass