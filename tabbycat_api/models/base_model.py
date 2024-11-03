import dataclasses
import inspect
from typing import Any, ClassVar, TypeVar, Iterable
from urllib.parse import urlparse
from ..exceptions import TabbycatException

T = TypeVar("T", bound="BaseModel")

@dataclasses.dataclass
class BaseModel:
    client: Any = dataclasses.field(default=None, kw_only=True, repr=False)
    loaded: bool = dataclasses.field(default=False, kw_only=True, repr=False)
    to_cache: dataclasses.InitVar[bool] = dataclasses.field(default=False, kw_only=True)
    cache: Any = dataclasses.field(default=None, kw_only=True, repr=False)
    
    FIELDS_REQUIRED: ClassVar[list[str]] = []
    FIELDS_READONLY: ClassVar[list[str]] = ["client"]
    FIELDS_URL_STR: ClassVar[list[str]] = []
    FIELDS_URL_LIST: ClassVar[list[str]] = []

    def __post_init__(self, to_cache: bool) -> None:
        if to_cache and self.cache is not None:
            self.cache.set(self)
        field_dict = {f.name: getattr(self, f.name) for f in dataclasses.fields(self)}
        if "cache" in field_dict:
            del field_dict["cache"]
        self.update(**field_dict)

    def __hash__(self) -> int:
        if hasattr(self, "url"):
            return hash(self.url)
        else:
            raise TypeError(f"Class {self.__class__.__name__} is not hashable: missing url field")

    def update(self, **kwargs) -> None:
        field_types = {f.name: f.type for f in dataclasses.fields(self)}
        for key, value in kwargs.items():
            if key not in field_types:
                raise KeyError(f"{key} is not a valid field")
            if key in self.FIELDS_URL_STR and field_types[key] is str:
                setattr(self, key, urlparse(value).path if value else None)
            else:
                from ..client import get_model
                setattr(self, key, get_model(value, field_types[key], client=self.client, loaded=self.loaded, cache=self.cache))

    def _check_requestable(self) -> None:
        if not hasattr(self, "url"):
            raise TypeError(f"Class {self.__class__.__name__} is not fetchable: missing url field")
        if not self.url:
            raise ValueError(f"{self.__class__.__name__} object does not have a valid url")
        if not self.client:
            raise TabbycatException(f"{self.__class__.__name__} object does not have a valid client")
        return
    
    @classmethod
    def init_url(cls, client, url):
        return cls(client=client, url=url)

    def get_original_url(self) -> str:
        if not hasattr(self, "url"):
            raise TypeError(f"Class {self.__class__.__name__} is not fetchable: missing url field")
        if not self.url:
            raise ValueError("No url specified")
        return f"{self.client.base_url}{self.url}"

    async def fetch(self):
        self._check_requestable()
        response: dict = await self.client._get(self.url, None)
        self.update(**response, loaded=True)

    async def post(self):
        self._check_requestable()
        from ..utils.to_json import to_json
        response: dict = await self.client._post(self.url, to_json(self))
        self.update(**response)

    async def patch(self: T, new: T) -> T:
        self._check_requestable()
        from ..utils.to_json import to_json
        response: dict = await self.client._patch(self.url, to_json(new, include_required=False))
        self.update(**response)

    async def put(self: T, new: T) -> T:
        self._check_requestable()
        from ..utils.to_json import to_json
        response: dict = await self.client._put(self.url, to_json(new, include_required=False))
        self.update(**response)

    async def delete(self) -> None:
        self._check_requestable()
        await self.client._delete(self.url)
        for field in dataclasses.fields(self):
            delattr(self, field.name)