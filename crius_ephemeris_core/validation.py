"""
Runtime validation utilities using Pydantic (optional dependency).

This module provides Pydantic models for runtime validation of ephemeris types.
Pydantic is an optional dependency - if not installed, validation functions will
raise ImportError.

To use validation, install pydantic:
    pip install pydantic

Or install with validation support:
    pip install crius-ephemeris-core[validation]
"""

from typing import Optional, List, Literal, Dict, Any
from datetime import datetime

try:
    from pydantic import BaseModel, Field, field_validator
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    BaseModel = None  # type: ignore
    Field = None  # type: ignore
    field_validator = None  # type: ignore

from .types import (
    EphemerisSettings,
    GeoLocation,
    PlanetPosition,
    HousePositions,
    LayerPositions,
    LayerContext,
    VedicOptions,
)


def _check_pydantic():
    """Check if Pydantic is available, raise ImportError if not."""
    if not PYDANTIC_AVAILABLE:
        raise ImportError(
            "Pydantic is required for validation. Install it with: "
            "pip install pydantic"
            " or pip install crius-ephemeris-core[validation]"
        )


if PYDANTIC_AVAILABLE:
    class VedicOptionsModel(BaseModel):
        """Pydantic model for VedicOptions."""

        include_nakshatras: Optional[bool] = None
        enabled_vargas: Optional[List[str]] = None
        include_dashas: Optional[bool] = None
        dasha_systems: Optional[List[str]] = None
        dashas_depth: Optional[Literal["mahadasha", "antardasha", "pratyantardasha"]] = None
        include_yogas: Optional[bool] = None

        class Config:
            extra = "forbid"

    class EphemerisSettingsModel(BaseModel):
        """Pydantic model for EphemerisSettings."""

        zodiac_type: Literal["tropical", "sidereal"] = Field(
            ..., description="Zodiac type: tropical or sidereal"
        )
        ayanamsa: Optional[str] = Field(
            None, description="Ayanamsa for sidereal calculations"
        )
        house_system: str = Field(..., description="House system name")
        include_objects: List[str] = Field(..., description="List of objects to include")
        vedic_options: Optional[VedicOptionsModel] = None

        @field_validator("zodiac_type")
        @classmethod
        def validate_zodiac_type(cls, v: str) -> str:
            """Validate zodiac type."""
            if v not in ("tropical", "sidereal"):
                raise ValueError("zodiac_type must be 'tropical' or 'sidereal'")
            return v

        class Config:
            extra = "forbid"

    class GeoLocationModel(BaseModel):
        """Pydantic model for GeoLocation."""

        lat: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
        lon: float = Field(..., ge=-180, le=180, description="Longitude in degrees")

        class Config:
            extra = "forbid"

    class PlanetPositionModel(BaseModel):
        """Pydantic model for PlanetPosition."""

        lon: float = Field(..., ge=0, lt=360, description="Longitude in degrees (0-360)")
        lat: float = Field(..., description="Latitude in degrees")
        speed_lon: float = Field(..., description="Speed in longitude (degrees per day)")
        retrograde: bool = Field(..., description="Whether the planet is retrograde")

        class Config:
            extra = "forbid"

    class HousePositionsModel(BaseModel):
        """Pydantic model for HousePositions."""

        system: str = Field(..., description="House system name")
        cusps: Dict[str, float] = Field(..., description="House cusps: '1'..'12' -> degrees")
        angles: Dict[str, float] = Field(..., description="Angles: 'asc', 'mc', 'ic', 'dc' -> degrees")

        class Config:
            extra = "forbid"

    class LayerPositionsModel(BaseModel):
        """Pydantic model for LayerPositions."""

        planets: Dict[str, PlanetPositionModel] = Field(
            ..., description="Planet ID -> position"
        )
        houses: Optional[HousePositionsModel] = Field(
            None, description="House positions (None if no location provided)"
        )

        class Config:
            extra = "forbid"

    class LayerContextModel(BaseModel):
        """Pydantic model for LayerContext."""

        layer_id: str = Field(..., description="Layer identifier")
        kind: str = Field(..., description="Layer kind (e.g., 'natal', 'transit')")
        datetime: datetime = Field(..., description="UTC datetime for calculation")
        location: Optional[GeoLocationModel] = Field(
            None, description="Geographic location"
        )
        settings: EphemerisSettingsModel = Field(..., description="Ephemeris settings")

        class Config:
            extra = "forbid"


def validate_ephemeris_settings(settings: Dict[str, Any]) -> EphemerisSettings:
    """
    Validate and normalize EphemerisSettings using Pydantic.

    Args:
        settings: Dictionary with ephemeris settings

    Returns:
        Validated EphemerisSettings dict

    Raises:
        ImportError: If Pydantic is not installed
        ValidationError: If settings are invalid
    """
    _check_pydantic()
    model = EphemerisSettingsModel(**settings)
    return model.model_dump(exclude_none=False)


def validate_geo_location(location: Dict[str, Any]) -> GeoLocation:
    """
    Validate and normalize GeoLocation using Pydantic.

    Args:
        location: Dictionary with lat and lon

    Returns:
        Validated GeoLocation dict

    Raises:
        ImportError: If Pydantic is not installed
        ValidationError: If location is invalid
    """
    _check_pydantic()
    model = GeoLocationModel(**location)
    return model.model_dump(exclude_none=False)


def validate_layer_positions(positions: Dict[str, Any]) -> LayerPositions:
    """
    Validate and normalize LayerPositions using Pydantic.

    Args:
        positions: Dictionary with planets and optionally houses

    Returns:
        Validated LayerPositions dict

    Raises:
        ImportError: If Pydantic is not installed
        ValidationError: If positions are invalid
    """
    _check_pydantic()
    model = LayerPositionsModel(**positions)
    return model.model_dump(exclude_none=False)


def validate_layer_context(context: Dict[str, Any]) -> LayerContext:
    """
    Validate and normalize LayerContext using Pydantic.

    Args:
        context: Dictionary with layer context

    Returns:
        Validated LayerContext dict

    Raises:
        ImportError: If Pydantic is not installed
        ValidationError: If context is invalid
    """
    _check_pydantic()
    model = LayerContextModel(**context)
    return model.model_dump(exclude_none=False)


def validate_planet_position(position: Dict[str, Any]) -> PlanetPosition:
    """
    Validate and normalize PlanetPosition using Pydantic.

    Args:
        position: Dictionary with planet position data

    Returns:
        Validated PlanetPosition dict

    Raises:
        ImportError: If Pydantic is not installed
        ValidationError: If position is invalid
    """
    _check_pydantic()
    model = PlanetPositionModel(**position)
    return model.model_dump(exclude_none=False)


def validate_house_positions(houses: Dict[str, Any]) -> HousePositions:
    """
    Validate and normalize HousePositions using Pydantic.

    Args:
        houses: Dictionary with house positions

    Returns:
        Validated HousePositions dict

    Raises:
        ImportError: If Pydantic is not installed
        ValidationError: If houses are invalid
    """
    _check_pydantic()
    model = HousePositionsModel(**houses)
    return model.model_dump(exclude_none=False)

