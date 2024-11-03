import httpx
import logging
import asyncio
from urllib.parse import urlparse
from .utils import route_class, create_url, to_json
import types
from typing import get_origin, get_args, Any, Literal, TypeVar
from json.decoder import JSONDecodeError

from .models.enums import TeamStandingsMetricEnum, SpeakerStandingsMetricEnum
from .exceptions import TabbycatException
from .my_types import UrlStr, NULL
from .client_cache import BaseCache
from . import models
from .models import *

T = TypeVar("T", bound=BaseModel)

def replace_null_recursive(obj_: Any):
    if isinstance(obj_, dict):
        return {k: replace_null_recursive(v) for k, v in obj_.items()}
    if isinstance(obj_, list):
        return [replace_null_recursive(i) for i in obj_]
    return NULL if obj_ is None else obj_

def need_type_conversion(type_: type):
    if type_ is Any:
        return False
    origin = get_origin(type_)
    if origin is None:
        return issubclass(type_, BaseModel) if not isinstance(type_, str) else True
    if origin is types.UnionType:
        return any(need_type_conversion(i) for i in get_args(type_))
    if origin is Literal:
        return False
    return False

def get_model(object_: Any, type_: type = None, client: "Client" = None, cache: BaseCache = None, loaded: bool = True):
    if object_ is None or object_ == NULL or isinstance(object_, BaseModel) or type_ is Any:
        return object_
    if isinstance(object_, list):
        return [get_model(i, get_args(type_)[0], client=client, cache=cache, loaded=loaded) for i in object_]
    if not need_type_conversion(type_):
        return object_
    if isinstance(object_, str):
        object_ = {"url": object_}
        loaded = False
    if get_origin(type_) is types.UnionType or type_ is BaseModel or type_ is PaginatedModel:
        type_ = route_class(object_["url"])
    if isinstance(type_, str): # string to stop circular imports
        type_ = getattr(models, type_)
    # Extract only the path part or URL
    if "url" in object_:
        object_["url"] = urlparse(object_["url"]).path
    # Check if cachable type
    if cache is None:
        return type_(client=client, loaded=loaded, **object_)
    if not cache.is_cachable(type_):
        return type_(client=client, loaded=loaded, cache=cache, **object_)
    # Check if cache exists
    cached_obj = cache.get(type_, object_["url"])
    if cached_obj is None:
        cached_obj = type_(client=client, loaded=loaded, cache=cache, to_cache=True, **object_)
    else:
        cached_obj.update(loaded=cached_obj.loaded or loaded, **object_)
    return cached_obj

class Client:
    def __init__(self, base_url: str, token: str, tournament_slug: str, editable: bool=False, semaphore:int=10, logger: logging.Logger=None, cache: BaseCache = None):
        base_url = urlparse(base_url)
        self.base_url = f"{base_url.scheme}://{base_url.netloc}"
        self.token = token
        self.tournament_slug = tournament_slug
        self.editable = editable
        self.semaphore = asyncio.Semaphore(semaphore)
        self.logger = logger or logging.getLogger(__name__)
        self.session = httpx.AsyncClient(headers={"Authorization": f"Token {self.token}"}, base_url=self.base_url)
        self._cache: BaseCache = cache

    @property
    def client(self) -> "Client":
        return self

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self.session.aclose()

    async def close(self):
        await self.session.aclose()

    async def _request(self, url: UrlStr, method: Literal["get", "post", "put", "patch", "delete"], json=None, params=None, **kwargs):
        params = {k: v for k, v in params.items() if v is not None} if params is not None else None
        async with self.semaphore:
            self.logger.info(f"[{method.upper()} {url}] params = {params}, JSON = {json}")
            response = await self.session.request(method, url, params=params, json=json, **kwargs)
            if response.status_code < 200 or response.status_code >= 300:
                self.logger.error(f"[{method.upper()} {url}] {response.status_code} {response.text}")
                raise TabbycatException(response.text)
            self.logger.debug(f"[{method.upper()} {url}] {response.status_code}")
            try:
                json = response.json()
            except JSONDecodeError:
                return None
        return replace_null_recursive(json)

    async def _get(self, url: UrlStr, params=None, **kwargs):
        return await self._request(url, "get", params=params, **kwargs)
    
    async def _post(self, url: UrlStr, json=None, **kwargs):
        if not self.editable:
            raise TabbycatException("Client is not editable")
        return await self._request(url, "post", json=json, **kwargs)
    
    async def _patch(self, url: UrlStr, json=None, **kwargs):
        if not self.editable:
            raise TabbycatException("Client is not editable")
        return await self._request(url, "patch", json=json, **kwargs)

    async def _put(self, url: UrlStr, json=None, **kwargs):
        if not self.editable:
            raise TabbycatException("Client is not editable")
        return await self._request(url, "put", json=json, **kwargs)

    async def _delete(self, url: UrlStr, **kwargs):
        if not self.editable:
            raise TabbycatException("Client is not editable")
        return await self._request(url, "delete", **kwargs)

    async def create(self, object_: T) -> T:
        if not self.editable:
            raise TabbycatException("Client does not have permission to edit data")
        if type(object_) not in create_url: #TODO: add all
            raise TabbycatException(f"Cannot create type {type(object_).__name__}")
        if object_.url is not None:
            raise TabbycatException("Cannot create object with existing URL")
        post_path = create_url[type(object_)].format(tournament_slug=self.tournament_slug)
        json = to_json(object_)
        response = await self._post(post_path, json=json)
        return get_model(response, type(object_), self, self._cache)

    async def update_post(self, object_: T) -> T:
        await object_.post()
        return object_
    
    async def update_patch(self, object_: T, new: T) -> T:
        await object_.patch(new=new)
        return object_

    async def get_model(self, path: str, type_: type[T], fetch_if_unloaded: bool = True, **kwargs) -> T:
        object_ = get_model(object_=path, type_=type_, client=self, cache=self._cache, loaded=False)
        if not object_.loaded and fetch_if_unloaded:
            await object_.fetch(**kwargs)
        return object_

    async def get_tournament(self) -> Tournament:
        return await self.get_model(f"/api/v1/tournaments/{self.tournament_slug}", Tournament)

    async def get_institutions(self) -> PaginatedInstitutions:
        return await self.get_model("/api/v1/institutions", PaginatedInstitutions)

    async def get_institution(self, id: int) -> Institution:
        return await self.get_model(f"/api/v1/institutions/{id}", Institution)

    async def get_adjudicators(self) -> PaginatedAdjudicators:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/adjudicators", PaginatedAdjudicators)
    
    async def get_adjudicator(self, id: int) -> Adjudicator:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/adjudicators/{id}", Adjudicator)
    
    async def get_break_categories(self) -> PaginatedBreakCategories:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/break-categories", PaginatedBreakCategories)
    
    async def get_break_category(self, id: int) -> BreakCategory:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/break-categories/{id}", BreakCategory)
    
    async def get_teams(self) -> PaginatedTeams:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/teams", PaginatedTeams)
    
    async def get_team(self, id: int) -> Team:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/teams/{id}", Team)
    
    async def get_team_standings(self, category: int = None, round: int = None, metrics: list[TeamStandingsMetricEnum] = None, extra_metrics: list[TeamStandingsMetricEnum] = None):
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/teams/standings", PaginatedTeamStandings, category=category, round=round, metrics=metrics, extra_metrics=extra_metrics)
    
    async def get_team_round_scores(self) -> PaginatedTeamRoundScores:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/teams/standings/rounds", PaginatedTeamRoundScores)
    
    async def get_speaker_categories(self) -> PaginatedSpeakerCategories:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/speaker-categories", PaginatedSpeakerCategories)
    
    async def get_speaker_category(self, id: int) -> SpeakerCategory:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/speaker-categories/{id}", SpeakerCategory)
    
    async def get_speakers(self) -> PaginatedSpeakers:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/speakers", PaginatedSpeakers)
    
    async def get_speaker(self, id: int) -> Speaker:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/speakers/{id}", Speaker)
    
    async def get_speaker_standings(self, category: int = None, round: int = None, metrics: list[SpeakerStandingsMetricEnum] = None, extra_metrics: list[SpeakerStandingsMetricEnum] = None) -> PaginatedSpeakerStandings:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/speakers/standings", PaginatedSpeakerStandings, category=category, round=round, metrics=metrics, extra_metrics=extra_metrics)
    
    async def get_speaker_round_scores(self) -> PaginatedSpeakerRoundScores:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/speakers/standings/rounds", PaginatedSpeakerRoundScores)
    
    async def get_venues(self) -> PaginatedVenues:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/venues", PaginatedVenues)
    
    async def get_venue(self, id: int) -> Venue:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/venues/{id}", Venue)
    
    async def get_rounds(self) -> PaginatedRounds:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/rounds", PaginatedRounds)
    
    async def get_round(self, seq: int) -> Round:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/rounds/{seq}", Round)
    
    async def get_debates(self, round_seq: int) -> PaginatedRoundPairings:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/rounds/{round_seq}/pairings", PaginatedRoundPairings)
    
    async def get_ballots(self, round_seq: int, debate_pk: int, confirmed: bool = None) -> PaginatedBallots:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/rounds/{round_seq}/pairings/{debate_pk}/ballots", PaginatedBallots, confirmed=confirmed)
    
    async def get_feedbacks(self, round: list[int] = None, source_type: Literal["adjudicator", "team"] = None, source: int = None, target: int = None, **kwargs) -> PaginatedFeedbacks:
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/feedback", PaginatedFeedbacks, round=round, source_type=source_type, source=source, target=target, **kwargs)
    
    async def get_preferences(self):
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/preferences", PaginatedPreferences)
    
    async def get_preference(self, id: str):
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/preferences/{id}", Preference)
    
    async def get_feedback_questions(self):
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/feedback-questions", PaginatedFeedbackQuestions)
    
    async def get_feedback_question(self, id: int):
        return await self.get_model(f"api/v1/tournaments/{self.tournament_slug}/feedback-questions/{id}", FeedbackQuestion)