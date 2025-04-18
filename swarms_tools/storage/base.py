from typing import Any
from abc import ABC, abstractmethod


class BaseStorageClient(ABC):
    """Abstract base class defining an interface for key-value storage clients.

    This class provides a standard interface for interacting with various storage backends
    (e.g., in-memory, Redis, or database) using both synchronous and asynchronous methods.
    Subclasses must implement all abstract methods to provide concrete storage functionality.
    """

    @abstractmethod
    def get(self, key: str) -> Any | None:
        """Synchronously retrieve a value associated with the given key.

        Args:
            key (str): The key to look up in the storage.

        Returns:
            Any | None: The value associated with the key, or None if the key does not exist.
        """
        ...

    @abstractmethod
    async def aget(self, key: str) -> Any | None:
        """Asynchronously retrieve a value associated with the given key.

        Args:
            key (str): The key to look up in the storage.

        Returns:
            Any | None: The value associated with the key, or None if the key does not exist.
        """
        ...

    @abstractmethod
    def put(self, key: str, value: Any) -> Any | None:
        """Synchronously store a value associated with the given key.

        Args:
            key (str): The key under which the value is stored.
            value (Any): The value to store, which can be of any type.

        Returns:
            Any | None: The stored value or None, depending on the implementation.
        """
        ...

    @abstractmethod
    async def aput(self, key: str, value: Any) -> Any | None:
        """Asynchronously store a value associated with the given key.

        Args:
            key (str): The key under which the value is stored.
            value (Any): The value to store, which can be of any type.

        Returns:
            Any | None: The stored value or None, depending on the implementation.
        """
        ...
