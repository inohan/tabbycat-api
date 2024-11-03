from __future__ import annotations

from ..models import *
from ..my_types import UrlStr
from urllib.parse import urlparse
import parse
import re

class RouteException(Exception):
    pass

def route_class(path: UrlStr) -> type:
    path = urlparse(path).path
    chunks = re.findall(r'(/[^/]+)', path)
    path_params = {}
    return route_recursive(chunks, route_graph, path_params)

def route_recursive(chunks: list[str], route: tuple, path_params: dict):
    for path, handler in route:
        if path == "":
            if not chunks:
                return handler
            continue
        match_result = parse.parse(path, chunks[0])
        if match_result is not None:
            path_params.update(match_result.named)
            if type(handler) is tuple:
                return route_recursive(chunks[1:], handler, path_params)
            else:
                return handler
    raise RouteException(f"Could not find route for path {chunks}")



route_graph = (
    ("/api", (
        ("", Root),
        ("/v1", (
            ("", V1Root),
            ("/institutions", (
                ("", PaginatedInstitutions),
                ("/{id:d}", Institution)
            )),
            ("/tournaments", (
                ("", PaginatedTournaments),
                ("/{tournament_slug}", (
                    ("", Tournament),
                    ("/adjudicators", (
                        ("", PaginatedAdjudicators),
                        ("/{id:d}", (
                            ("", Adjudicator),
                            ("/checkin", Checkin)
                        ))
                    )),
                    ("/break-categories", (
                        ("", PaginatedBreakCategories),
                        ("/{id:d}", (
                            ("", BreakCategory),
                            ("/break", PaginatedBreakingTeams),
                            ("/eligibility", BreakEligibility)
                        ))
                    )),
                    ("/feedback", (
                        ("", PaginatedFeedbacks),
                        ("/{id:d}", Feedback)
                    )),
                    ("/feedback-questions", (
                        ("", PaginatedFeedbackQuestions),
                        ("/{id:d}", FeedbackQuestion)
                    )),
                    ("/institutions", PaginatedPerTourInstitutions),
                    ("/motions", (
                        ("", PaginatedMotions),
                        ("/{id:d}", Motion)
                    )),
                    ("/preferences", (
                        ("", PaginatedPreferences),
                        ("/bulk", None), #TODO: implement
                        ("/{id:d}", Preference),
                    )),
                    ("/rounds", (
                        ("", PaginatedRounds),
                        ("/{round_seq:d}", (
                            ("", Round),
                            ("/availabilities", PaginatedAvailabilities),
                            ("/pairings", (
                                ("", PaginatedRoundPairings),
                                ("/{debate_pk:d}", (
                                    ("", RoundPairing),
                                    ("/ballots", (
                                        ("", PaginatedBallots),
                                        ("/{id:d}", Ballot)
                                    ))
                                ))
                            )),
                            ("preformed-panels", (
                                ("", PaginatedPreformedPanels),
                                ("/{debate_pk:d}", PreformedPanel)
                            ))
                        ))
                    )),
                    ("/speaker-categories", (
                        ("", PaginatedSpeakerCategories),
                        ("/{id:d}", (
                            ("", SpeakerCategory),
                            ("/eligibility", SpeakerEligibility)
                        ))
                    )),
                    ("/speakers", (
                        ("", PaginatedSpeakers),
                        ("/standings", (
                            ("", PaginatedSpeakerStandings),
                            ("/replies", PaginatedSpeakerStandings),
                            ("/rounds", PaginatedSpeakerRoundScores)
                        )),
                        ("/{id:d}", (
                            ("", Speaker),
                            ("/checkin", Checkin)
                        ))
                    )),
                    ("/teams", (
                        ("", PaginatedTeams),
                        ("/standings", (
                            ("", PaginatedTeamStandings),
                            ("/rounds", PaginatedTeamRoundScores)
                        )),
                        ("/{id:d}", Team)
                    )),
                    ("/venue-categories", (
                        ("", PaginatedVenueCategories),
                        ("/{id:d}", VenueCategory)
                    )),
                    ("/venues", (
                        ("", PaginatedVenues),
                        ("/{id:d}", (
                            ("", Venue),
                            ("/checkin", Checkin)
                        ))
                    )),
                    ("/user-groups", (
                        ("", PaginatedGroups),
                        ("/{id:d}", Group)
                    ))
                ))
            )),
            ("/users", (
                ("", PaginatedUsers),
                ("/{id}", User)
            ))
        ))
    )),
)

create_url: dict[BaseModel, str] = {
    Institution: "/api/v1/institutions",
    Adjudicator: "/api/v1/tournaments/{tournament_slug}/adjudicators",
    BreakCategory: "/api/v1/tournaments/{tournament_slug}/break-categories",
    Team: "/api/v1/tournaments/{tournament_slug}/teams",
    Speaker: "/api/v1/tournaments/{tournament_slug}/speakers",
    SpeakerCategory: "/api/v1/tournaments/{tournament_slug}/speaker-categories",
    Venue: "/api/v1/tournaments/{tournament_slug}/venues",
    VenueCategory: "/api/v1/tournaments/{tournament_slug}/venue-categories",
}

cachable = {
    Root,
    V1Root,
    Institution,
    Tournament,
    Adjudicator,
    Checkin,
    BreakCategory,
    BreakEligibility,
    Feedback,
    FeedbackQuestion,
    Motion,
    Round,
    RoundPairing,
    Ballot,
    PreformedPanel,
    SpeakerCategory,
    Speaker,
    Team,
    VenueCategory,
    Venue,
    Group,
    User
}