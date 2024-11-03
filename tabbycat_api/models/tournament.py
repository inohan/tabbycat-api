from dataclasses import dataclass
from .base_model import BaseModel
from .paginated_model import PaginatedModel

from .round import Round, PaginatedRounds
from .break_category import PaginatedBreakCategories
from .speaker_category import PaginatedSpeakerCategories
from .per_tournament_institution import PaginatedPerTourInstitutions
from .team import PaginatedTeams
from .adjudicator import PaginatedAdjudicators
from .speaker import PaginatedSpeakers
from .venue import PaginatedVenues
from .venue_category import PaginatedVenueCategories
from .motion import PaginatedMotions
from .feedback import PaginatedFeedbacks
from .feedback_question import PaginatedFeedbackQuestions
from .preference import PaginatedPreferences

@dataclass
class TournamentLinks(BaseModel):
    rounds: PaginatedRounds = None
    break_categories: PaginatedBreakCategories = None
    speaker_categories: PaginatedSpeakerCategories = None
    institutions: PaginatedPerTourInstitutions = None
    teams: PaginatedTeams = None
    adjudicators: PaginatedAdjudicators = None
    speakers: PaginatedSpeakers = None
    venues: PaginatedVenues = None
    venue_categories: PaginatedVenueCategories = None
    motions: PaginatedMotions = None
    feedback: PaginatedFeedbacks = None
    feedback_questions: PaginatedFeedbackQuestions = None
    preferences: PaginatedPreferences = None
    
    FIELDS_REQUIRED = ["rounds", "break_categories", "speaker_categories", "institutions", "teams", "adjudicators", "speakers", "venues", "venue_categories", "motions", "feedback", "feedback_questions", "preferences"]
    FIELDS_READONLY = ["rounds", "break_categories", "speaker_categories", "institutions", "teams", "adjudicators", "speakers", "venues", "venue_categories", "motions", "feedback", "feedback_questions", "preferences"]
    FIELDS_URL_STR = ["rounds", "break_categories", "speaker_categories", "institutions", "teams", "adjudicators", "speakers", "venues", "venue_categories", "motions", "feedback", "feedback_questions", "preferences"]
    
@dataclass
class Tournament(BaseModel):
    id: int = None
    url: str = None
    current_rounds: list[Round] = None
    _links: TournamentLinks = None
    name: str = None
    short_name: str = None
    seq: int = None
    slug: str = None
    active: bool = None
    
    FIELDS_REQUIRED = ["id", "url", "current_rounds", "_links", "name", "slug"]
    FIELDS_READONLY = ["id", "url", "current_rounds", "_links"]
    FIELDS_URL_STR = ["url"]
    FIELDS_URL_LIST = ["current_rounds"]

@dataclass
class PaginatedTournaments(PaginatedModel[Tournament]):
    pass