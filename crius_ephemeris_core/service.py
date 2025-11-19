"""
Core service interfaces for ephemeris calculations.

This module provides abstract base classes and service patterns for ephemeris
calculations. These are optional interfaces that can be used to build service
layers on top of adapters.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Protocol

from .types import (
    EphemerisSettings,
    GeoLocation,
    LayerPositions,
    LayerContext,
)
from .protocols import EphemerisAdapter


class EphemerisService(ABC):
    """
    Abstract base class for ephemeris services.

    Services provide a higher-level interface than adapters, potentially
    including caching, error handling, logging, and other cross-cutting concerns.
    """

    @abstractmethod
    def get_positions(
        self,
        dt_utc: datetime,
        location: Optional[GeoLocation],
        settings: EphemerisSettings,
    ) -> LayerPositions:
        """
        Get ephemeris positions for a given datetime and location.

        Args:
            dt_utc: UTC datetime for calculation
            location: Optional geographic location (required for houses)
            settings: Ephemeris calculation settings

        Returns:
            LayerPositions with planetary and optionally house positions

        Raises:
            Various exceptions depending on implementation
        """
        pass

    @abstractmethod
    def get_positions_for_context(self, context: LayerContext) -> LayerPositions:
        """
        Get ephemeris positions from a LayerContext.

        Args:
            context: LayerContext with all calculation parameters

        Returns:
            LayerPositions with planetary and optionally house positions

        Raises:
            Various exceptions depending on implementation
        """
        pass


class BaseEphemerisService(EphemerisService):
    """
    Base implementation of EphemerisService.

    Provides common patterns like adapter delegation and basic error handling.
    Subclasses can override methods to add caching, logging, etc.
    """

    def __init__(self, adapter: EphemerisAdapter):
        """
        Initialize service with an adapter.

        Args:
            adapter: EphemerisAdapter instance to use for calculations
        """
        self.adapter = adapter

    def get_positions(
        self,
        dt_utc: datetime,
        location: Optional[GeoLocation],
        settings: EphemerisSettings,
    ) -> LayerPositions:
        """
        Get ephemeris positions by delegating to adapter.

        Subclasses can override to add caching, logging, etc.
        """
        return self.adapter.calc_positions(dt_utc, location, settings)

    def get_positions_for_context(self, context: LayerContext) -> LayerPositions:
        """
        Get ephemeris positions from a LayerContext.

        Extracts parameters from context and calls get_positions.
        """
        return self.get_positions(
            context["datetime"],
            context["location"],
            context["settings"],
        )


class CacheProvider(Protocol):
    """
    Protocol for cache providers.

    Implementations can provide different caching strategies
    (in-memory, Redis, etc.).
    """

    def get(self, key: str) -> Optional[LayerPositions]:
        """Get cached value by key."""
        ...

    def set(self, key: str, value: LayerPositions) -> None:
        """Set cached value."""
        ...

    def clear(self) -> None:
        """Clear all cached values."""
        ...


class CachedEphemerisService(BaseEphemerisService):
    """
    EphemerisService with caching support.

    Uses a CacheProvider to cache calculation results.
    """

    def __init__(
        self,
        adapter: EphemerisAdapter,
        cache: Optional[CacheProvider] = None,
        cache_key_fn: Optional[callable] = None,
    ):
        """
        Initialize cached service.

        Args:
            adapter: EphemerisAdapter instance
            cache: Optional CacheProvider instance
            cache_key_fn: Optional function to generate cache keys
        """
        super().__init__(adapter)
        self.cache = cache
        self.cache_key_fn = cache_key_fn or self._default_cache_key

    def _default_cache_key(
        self,
        dt_utc: datetime,
        location: Optional[GeoLocation],
        settings: EphemerisSettings,
    ) -> str:
        """Generate default cache key from parameters."""
        location_str = f"{location['lat']},{location['lon']}" if location else "None"
        settings_str = f"{settings['zodiac_type']}:{settings['house_system']}"
        objects_str = ",".join(sorted(settings.get("include_objects", [])))
        return f"{dt_utc.isoformat()}:{location_str}:{settings_str}:{objects_str}"

    def get_positions(
        self,
        dt_utc: datetime,
        location: Optional[GeoLocation],
        settings: EphemerisSettings,
    ) -> LayerPositions:
        """
        Get positions with caching.

        Checks cache first, then calculates if not found.
        """
        if self.cache is None:
            return super().get_positions(dt_utc, location, settings)

        cache_key = self.cache_key_fn(dt_utc, location, settings)
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        positions = super().get_positions(dt_utc, location, settings)
        self.cache.set(cache_key, positions)
        return positions


def create_ephemeris_service(
    adapter: EphemerisAdapter,
    enable_cache: bool = False,
    cache: Optional[CacheProvider] = None,
) -> EphemerisService:
    """
    Factory function to create an EphemerisService.

    Args:
        adapter: EphemerisAdapter instance
        enable_cache: Whether to enable caching
        cache: Optional CacheProvider (required if enable_cache is True)

    Returns:
        EphemerisService instance

    Raises:
        ValueError: If enable_cache is True but cache is None
    """
    if enable_cache:
        if cache is None:
            raise ValueError("cache must be provided when enable_cache is True")
        return CachedEphemerisService(adapter, cache=cache)
    return BaseEphemerisService(adapter)

