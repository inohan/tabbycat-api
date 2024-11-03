from dataclasses import dataclass
from .paginated_model import PaginatedModel

from .adjudicator import Adjudicator
from .team import Team
from .venue import Venue

@dataclass
class PaginatedAvailabilities(PaginatedModel[Adjudicator | Team | Venue]):
    FIELDS_URL_LIST = ["_data"]
    
    async def fetch(self, adjudicators: bool = True, teams: bool = True, venues: bool = True, **kwargs):
        return await super().fetch(params={"adjudicators": adjudicators, "teams": teams, "venues": venues}, **kwargs)
    
    async def post(self, objects: list[Adjudicator | Team | Venue]):
        """Mark objects as unavailable

        Args:
            objects (list[Adjudicator  |  Team  |  Venue]): objects to mark as unavailable
        """
        self._check_requestable()
        post_json = [obj_.url if isinstance(obj_, Adjudicator | Team | Venue) else obj_ for obj_ in objects]
        response: list = await self.client._post(self.url, json=post_json)
        self.update(_data = response)

    async def put(self, objects: list[Adjudicator | Team | Venue]):
        """Mark objects as available

        Args:
            objects (list[Adjudicator  |  Team  |  Venue]): objects to mark as available
        """
        self._check_requestable()
        post_json = [obj_.url if isinstance(obj_, Adjudicator | Team | Venue) else obj_ for obj_ in objects]
        response: list = await self.client._put(self.url, json=post_json)
        self.update(_data = response)

    async def patch(self, objects: list[Adjudicator | Team | Venue]):
        """Toggle the availabilities of the included objects

        Args:
            objects (list[Adjudicator  |  Team  |  Venue]): objects to toggle availability
        """
        self._check_requestable()
        post_json = [obj_.url if isinstance(obj_, Adjudicator | Team | Venue) else obj_ for obj_ in objects]
        response: list = await self.client._patch(self.url, json=post_json)
        self.update(_data = response)