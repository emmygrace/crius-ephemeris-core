"""
Crius Ephemeris Core - Pure ephemeris types and interfaces.

Named after Crius, the Titan of constellations and measuring the year.
"""

from .types import (
    EphemerisSettings,
    GeoLocation,
    PlanetPosition,
    HousePositions,
    LayerPositions,
    LayerContext,
)

from .protocols import EphemerisAdapter

__all__ = [
    "EphemerisSettings",
    "GeoLocation",
    "PlanetPosition",
    "HousePositions",
    "LayerPositions",
    "LayerContext",
    "EphemerisAdapter",
]

__version__ = "0.1.0"

