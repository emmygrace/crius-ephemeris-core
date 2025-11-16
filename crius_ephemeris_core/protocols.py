"""
Protocol definitions for ephemeris adapters.

These protocols define the interface that ephemeris adapter implementations must conform to.
"""

from datetime import datetime
from typing import Protocol, Optional

from .types import EphemerisSettings, GeoLocation, LayerPositions


class EphemerisAdapter(Protocol):
    """
    Protocol for ephemeris calculation adapters.

    Implementations of this protocol provide ephemeris calculations
    using various underlying libraries (Swiss Ephemeris, PyEphem, etc.).
    """

    def calc_positions(
        self,
        dt_utc: datetime,
        location: Optional[GeoLocation],
        settings: EphemerisSettings,
    ) -> LayerPositions:
        """
        Calculate planetary and house positions for a given datetime and location.

        Args:
            dt_utc: UTC datetime for the calculation
            location: Optional geographic location (required for house calculations)
            settings: Ephemeris calculation settings

        Returns:
            LayerPositions containing planetary positions and optionally house positions

        Raises:
            Various exceptions depending on implementation (e.g., if ephemeris data
            is missing or calculation fails)
        """
        ...

