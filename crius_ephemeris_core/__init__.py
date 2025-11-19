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
    VedicOptions,
)

from .protocols import EphemerisAdapter

# Optional service imports (can be imported separately)
try:
    from .service import (
        EphemerisService,
        BaseEphemerisService,
        CachedEphemerisService,
        CacheProvider,
        create_ephemeris_service,
    )
    _SERVICE_AVAILABLE = True
except ImportError:
    _SERVICE_AVAILABLE = False

__all__ = [
    "EphemerisSettings",
    "GeoLocation",
    "PlanetPosition",
    "HousePositions",
    "LayerPositions",
    "LayerContext",
    "EphemerisAdapter",
    "VedicOptions",
]

# Add service exports if available
if _SERVICE_AVAILABLE:
    __all__.extend([
        "EphemerisService",
        "BaseEphemerisService",
        "CachedEphemerisService",
        "CacheProvider",
        "create_ephemeris_service",
    ])

__version__ = "0.1.0"

