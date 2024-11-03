from dataclasses import dataclass
from typing import Generic, TypeVar, Iterator, get_args

from .base_model import BaseModel

T = TypeVar("T", bound=BaseModel)

@dataclass
class PaginatedModel(Generic[T], BaseModel):
    url: str = None
    _data: list[T] = None
    
    FIELDS_URL_STR = ["url"]
    
    def update(self, **kwargs):
        if "client" in kwargs:
            self.client = kwargs["client"]
            del kwargs["client"]
        if "loaded" in kwargs:
            self.loaded = kwargs["loaded"]
            del kwargs["loaded"]
        if "url" in kwargs:
            self.url = kwargs["url"]
            del kwargs["url"]
        if "_data" in kwargs:
            convert_base = get_args(self.__class__.__orig_bases__[0])[0]
            from ..client import get_model
            self._data = get_model(kwargs["_data"], list[convert_base], client=self.client, cache=self.cache)
            del kwargs["_data"]
        if kwargs:
            raise ValueError(f"{kwargs.keys()} is not a valid field")
    
    async def fetch(self, params = None, **kwargs) -> None:
        if not hasattr(self, "url"):
            raise TypeError(f"Class {self.__class__.__name__} is not fetchable")
        if not self.url:
            raise ValueError(f"Class {self.__class__.__name__} does not have a valid url")
        response: list = await self.client._get(self.url, params = params, **kwargs)
        return self.update(_data = response, loaded=True)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._data)