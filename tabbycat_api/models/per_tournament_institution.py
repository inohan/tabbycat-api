from dataclasses import dataclass
from .paginated_model import PaginatedModel

from .institution import Institution
from .team import Team
from .adjudicator import Adjudicator

@dataclass
class PerTournamentInstitution(Institution):
    teams: list[Team] = None
    adjudicators: list[Adjudicator] = None
    FIELDS_REQUIRED = ["id", "url", "name", "code"]
    FIELDS_READONLY = ["id", "url"]
    FIELDS_URL_LIST = ["teams", "adjudicators"]
    
    async def fetch(self):
        raise AttributeError("PerTournamentInstitution does not support fetch")

@dataclass
class PaginatedPerTourInstitutions(PaginatedModel[PerTournamentInstitution]):
    pass