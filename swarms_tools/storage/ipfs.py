import os
import io
from typing import overload
from types import TracebackType
from urllib.parse import urljoin

import httpx

from .base import BaseStorageClient


class IPFSStorageClient(BaseStorageClient):

    def __init__(
        self,
        rpc_url: str = os.getenv(
            "IPFS_RPC_URL", "http://127.0.0.1:5001"
        ),
        timeout: int | None = None,
    ):
        if not rpc_url.endswith("/"):
            rpc_url += "/"

        base_url = urljoin(rpc_url, "api/v0")
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
        )
        self._async_client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
        )

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        self._client.close()

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        await self._async_client.close()

    async def close(self):
        await self._async_client.aclose()

    async def aget(self, key: str) -> bytes:
        response = await self._async_client.post(
            "/cat", params={"arg": key}
        )
        response.raise_for_status()
        return response.content

    def get(self, key: str) -> bytes:
        response = self._client.post("/cat", params={"arg": key})
        response.raise_for_status()
        return response.content

    @overload
    async def aput(
        self, key: str, value: bytes
    ) -> str: ...  # pragma: no cover

    @overload
    async def aput(
        self, key: str, value: io.FileIO
    ) -> str: ...  # pragma: no cover

    async def aput(self, key: str, value) -> str:
        if isinstance(value, bytes):
            value = io.BytesIO(value)
        return await self._aput(key, value)

    async def _aput(self, key: str, file_: io.FileIO) -> str:
        files = {"file": (key, file_, "application/octet-stream")}
        response = await self._async_client.post("/add", files=files)
        response.raise_for_status()
        result = response.json()
        return result["Hash"]

    @overload
    async def put(
        self, key: str, value: bytes
    ) -> str: ...  # pragma: no cover

    @overload
    async def put(
        self, key: str, value: io.FileIO
    ) -> str: ...  # pragma: no cover

    def put(self, key: str, value) -> str:
        if isinstance(value, bytes):
            value = io.BytesIO(value)
        return self._put(key, value)

    def _put(self, key: str, file_: io.FileIO) -> str:
        files = {"file": (key, file_, "application/octet-stream")}
        response = self._client.post("/add", files=files)
        response.raise_for_status()
        result = response.json()
        return result["Hash"]
