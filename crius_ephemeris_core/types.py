"""
Core type definitions for ephemeris calculations.

These types are pure Python TypedDict definitions with no external dependencies.
"""

from datetime import datetime
from typing import TypedDict, Literal, Optional, List, NotRequired


class VedicOptions(TypedDict, total=False):
    """
    Optional configuration flags for Vedic/Jyotish calculations.

    These allow downstream services to request additional derived data
    such as divisional charts (vargas) or dasha timelines.
    """

    include_nakshatras: bool
    enabled_vargas: List[str]
    include_dashas: bool
    dasha_systems: List[str]
    dashas_depth: Literal["mahadasha", "antardasha", "pratyantardasha"]
    include_yogas: bool


class EphemerisSettings(TypedDict):
    """Settings for ephemeris calculations."""

    zodiac_type: Literal["tropical", "sidereal"]
    ayanamsa: Optional[str]
    house_system: str
    include_objects: list[str]
    vedic_options: NotRequired[VedicOptions]


class GeoLocation(TypedDict):
    """Geographic location coordinates."""

    lat: float
    lon: float


class PlanetPosition(TypedDict):
    """Planetary position data."""

    lon: float  # Longitude in degrees (0-360)
    lat: float  # Latitude in degrees
    speed_lon: float  # Speed in longitude (degrees per day)
    retrograde: bool  # Whether the planet is retrograde


class HousePositions(TypedDict):
    """House system positions."""

    system: str  # House system name
    cusps: dict[str, float]  # House cusps: "1".."12" -> degrees
    angles: dict[str, float]  # Angles: "asc", "mc", "ic", "dc" -> degrees


class LayerPositions(TypedDict):
    """Complete position data for a chart layer."""

    planets: dict[str, PlanetPosition]  # Planet ID -> position
    houses: Optional[HousePositions]  # House positions (None if no location provided)


class LayerContext(TypedDict):
    """Context for calculating positions for a chart layer."""

    layer_id: str
    kind: str
    datetime: datetime
    location: Optional[GeoLocation]
    settings: EphemerisSettings

