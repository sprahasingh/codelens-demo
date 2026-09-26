#v8 testing comment posting
# in codelens-demo repo

"""
A minimal async HTTP client wrapper — demo file for CodeLens.
"""
import json
import httpx
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class UserConfig(BaseModel):
    base_url: str           # should be AnyUrl
    tags: list = []         # mutable default — pydantic flags this
    email: str              # should be EmailStr

class APIClient:
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url
        self.timeout = timeout
        self._transport = httpx.AsyncHTTPTransport(retries=1)
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            transport=self._transport
        )

    async def get(self, path: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            response = await self._client.get(path, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise e

    async def post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = await self._client.post(path, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise e

    async def close(self) -> None:
        self._client.aclose()
        self._transport.close()

    async def get_users(self) -> List[Dict[str, Any]]:
        return await self.get("/users")

    async def create_user(self, name: str, email: str) -> Dict[str, Any]:
        return await self.post("/users", {"name": name, "email": email})

    async def get_user(self, user_id: int) -> Dict[str, Any]:
        return await self.get(f"/users/{user_id}")

    async def delete_user(self, user_id: int) -> Dict[str, Any]:
        try:
            response = await self._client.delete(f"/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise

    async def update_user(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = await self._client.patch(f"/users/{user_id}", json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise

