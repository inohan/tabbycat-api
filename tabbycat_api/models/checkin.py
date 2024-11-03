from dataclasses import dataclass, InitVar
from urllib.parse import urlparse
from .base_model import BaseModel

@dataclass
class Checkin(BaseModel):
    object: BaseModel = None
    barcode: str = None
    checked: bool = None
    timestamp: str = None
    url: str = None
    
    FIELDS_REQUIRED = ["object", "barcode", "checked", "timestamp"]
    FIELDS_READONLY = ["object", "url"]
    FIELDS_URL_STR = ["object", "url"]
    
    async def post(self):
        """Create object checkin identifier
        """
        self._check_requestable()
        response: dict = await self.client._post(self.url, None)
        self.update(**response)
    
    async def put(self, **kwargs):
        """Check in object
        """
        self._check_requestable()
        response: dict = await self.client._put(self.url, None)
        self.update(**response)
    
    async def patch(self, **kwargs):
        """Toggle object checkin status
        """
        self._check_requestable()
        response: dict = await self.client._patch(self.url, None)
        self.update(**response)
    
    async def delete(self):
        """Check out object
        """
        self._check_requestable()
        response: dict = await self.client._delete(self.url)
        self.update(**response)