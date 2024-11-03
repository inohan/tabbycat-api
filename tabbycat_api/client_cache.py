from collections import defaultdict
from typing import TypeVar
from .utils.route import cachable

T = TypeVar("T")

class BaseCache:
    _cachable: set[type] = set()
    
    def __init__(self) -> None:
        self._cache: defaultdict[type, dict[str, object]] = defaultdict(dict)
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} with {len(self)} entries>"

    def __len__(self) -> int:
        return sum([len(i) for i in self._cache.values()])

    def is_cachable(self, type_: type) -> bool:
        return type_ in cachable

    def get(self, type_: type[T], url: str) -> T | None:
        return self._cache[type_].get(url, None)
    
    def set(self, object_: object) -> None:
        self._cache[type(object_)][object_.url] = object_
    
    def delete(self, object_: object) -> None:
        del self._cache[type(object_)][object_.url]

class SimpleClientCache(BaseCache):
    _cachable = cachable