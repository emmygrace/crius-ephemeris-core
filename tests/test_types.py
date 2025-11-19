"""Unit tests for type definitions."""

import pytest
from typing import get_type_hints, get_origin, get_args
from datetime import datetime

from crius_ephemeris_core import (
    EphemerisSettings,
    GeoLocation,
    PlanetPosition,
    HousePositions,
    LayerPositions,
    LayerContext,
    VedicOptions,
)


class TestEphemerisSettings:
    """Test EphemerisSettings TypedDict."""

    def test_required_fields(self):
        """Test that required fields are present."""
        settings: EphemerisSettings = {
            "zodiac_type": "tropical",
            "ayanamsa": None,
            "house_system": "placidus",
            "include_objects": ["sun", "moon"],
        }
        assert settings["zodiac_type"] == "tropical"
        assert settings["house_system"] == "placidus"
        assert isinstance(settings["include_objects"], list)

    def test_zodiac_type_literal(self):
        """Test that zodiac_type accepts only valid literal values."""
        # Valid values
        settings_tropical: EphemerisSettings = {
            "zodiac_type": "tropical",
            "ayanamsa": None,
            "house_system": "placidus",
            "include_objects": [],
        }
        assert settings_tropical["zodiac_type"] == "tropical"

        settings_sidereal: EphemerisSettings = {
            "zodiac_type": "sidereal",
            "ayanamsa": "lahiri",
            "house_system": "placidus",
            "include_objects": [],
        }
        assert settings_sidereal["zodiac_type"] == "sidereal"

    def test_optional_vedic_options(self):
        """Test that vedic_options is optional."""
        settings_without_vedic: EphemerisSettings = {
            "zodiac_type": "tropical",
            "ayanamsa": None,
            "house_system": "placidus",
            "include_objects": [],
        }
        assert "vedic_options" not in settings_without_vedic

        settings_with_vedic: EphemerisSettings = {
            "zodiac_type": "tropical",
            "ayanamsa": None,
            "house_system": "placidus",
            "include_objects": [],
            "vedic_options": {
                "include_nakshatras": True,
                "enabled_vargas": ["d9"],
            },
        }
        assert "vedic_options" in settings_with_vedic
        assert settings_with_vedic["vedic_options"]["include_nakshatras"] is True


class TestGeoLocation:
    """Test GeoLocation TypedDict."""

    def test_required_fields(self):
        """Test that required fields are present."""
        location: GeoLocation = {
            "lat": 40.7128,
            "lon": -74.0060,
        }
        assert location["lat"] == 40.7128
        assert location["lon"] == -74.0060
        assert isinstance(location["lat"], float)
        assert isinstance(location["lon"], float)

    def test_numeric_types(self):
        """Test that lat and lon accept numeric types."""
        location_int: GeoLocation = {
            "lat": 40,
            "lon": -74,
        }
        assert location_int["lat"] == 40
        assert location_int["lon"] == -74


class TestPlanetPosition:
    """Test PlanetPosition TypedDict."""

    def test_required_fields(self):
        """Test that all required fields are present."""
        position: PlanetPosition = {
            "lon": 280.5,
            "lat": 0.0,
            "speed_lon": 1.0,
            "retrograde": False,
        }
        assert position["lon"] == 280.5
        assert position["lat"] == 0.0
        assert position["speed_lon"] == 1.0
        assert position["retrograde"] is False

    def test_longitude_range(self):
        """Test that longitude values are typically in 0-360 range."""
        position: PlanetPosition = {
            "lon": 380.5 % 360,  # Normalize to 0-360
            "lat": 0.0,
            "speed_lon": 1.0,
            "retrograde": False,
        }
        assert 0 <= position["lon"] < 360


class TestHousePositions:
    """Test HousePositions TypedDict."""

    def test_required_fields(self):
        """Test that all required fields are present."""
        houses: HousePositions = {
            "system": "placidus",
            "cusps": {"1": 15.0, "2": 45.0, "3": 75.0},
            "angles": {"asc": 15.0, "mc": 105.0, "ic": 285.0, "dc": 195.0},
        }
        assert houses["system"] == "placidus"
        assert isinstance(houses["cusps"], dict)
        assert isinstance(houses["angles"], dict)
        assert "asc" in houses["angles"]
        assert "mc" in houses["angles"]

    def test_cusp_structure(self):
        """Test that cusps use string keys for house numbers."""
        houses: HousePositions = {
            "system": "placidus",
            "cusps": {str(i): float(i * 30) for i in range(1, 13)},
            "angles": {"asc": 0.0, "mc": 0.0, "ic": 0.0, "dc": 0.0},
        }
        assert len(houses["cusps"]) == 12
        assert "1" in houses["cusps"]
        assert "12" in houses["cusps"]


class TestLayerPositions:
    """Test LayerPositions TypedDict."""

    def test_required_fields(self):
        """Test that all required fields are present."""
        positions: LayerPositions = {
            "planets": {
                "sun": {
                    "lon": 280.5,
                    "lat": 0.0,
                    "speed_lon": 1.0,
                    "retrograde": False,
                }
            },
            "houses": None,
        }
        assert "planets" in positions
        assert "houses" in positions
        assert positions["houses"] is None

    def test_with_houses(self):
        """Test LayerPositions with houses."""
        positions: LayerPositions = {
            "planets": {
                "sun": {
                    "lon": 280.5,
                    "lat": 0.0,
                    "speed_lon": 1.0,
                    "retrograde": False,
                }
            },
            "houses": {
                "system": "placidus",
                "cusps": {"1": 15.0},
                "angles": {"asc": 15.0, "mc": 105.0, "ic": 285.0, "dc": 195.0},
            },
        }
        assert positions["houses"] is not None
        assert positions["houses"]["system"] == "placidus"


class TestLayerContext:
    """Test LayerContext TypedDict."""

    def test_required_fields(self):
        """Test that all required fields are present."""
        dt = datetime(2024, 1, 1, 12, 0, 0)
        context: LayerContext = {
            "layer_id": "natal",
            "kind": "natal",
            "datetime": dt,
            "location": {"lat": 40.7128, "lon": -74.0060},
            "settings": {
                "zodiac_type": "tropical",
                "ayanamsa": None,
                "house_system": "placidus",
                "include_objects": ["sun"],
            },
        }
        assert context["layer_id"] == "natal"
        assert context["kind"] == "natal"
        assert isinstance(context["datetime"], datetime)
        assert context["location"] is not None
        assert context["settings"]["zodiac_type"] == "tropical"

    def test_optional_location(self):
        """Test that location can be None."""
        dt = datetime(2024, 1, 1, 12, 0, 0)
        context: LayerContext = {
            "layer_id": "transit",
            "kind": "transit",
            "datetime": dt,
            "location": None,
            "settings": {
                "zodiac_type": "tropical",
                "ayanamsa": None,
                "house_system": "placidus",
                "include_objects": ["sun"],
            },
        }
        assert context["location"] is None


class TestVedicOptions:
    """Test VedicOptions TypedDict."""

    def test_all_optional_fields(self):
        """Test that all fields in VedicOptions are optional."""
        # Empty dict should be valid
        vedic: VedicOptions = {}

        # Partial fields
        vedic_partial: VedicOptions = {
            "include_nakshatras": True,
        }

        # All fields
        vedic_full: VedicOptions = {
            "include_nakshatras": True,
            "enabled_vargas": ["d9", "d10"],
            "include_dashas": True,
            "dasha_systems": ["vimshottari"],
            "dashas_depth": "pratyantardasha",
            "include_yogas": False,
        }
        assert vedic_full["dashas_depth"] == "pratyantardasha"

    def test_dashas_depth_literal(self):
        """Test that dashas_depth accepts only valid literal values."""
        valid_depths = ["mahadasha", "antardasha", "pratyantardasha"]
        for depth in valid_depths:
            vedic: VedicOptions = {
                "dashas_depth": depth,
            }
            assert vedic["dashas_depth"] == depth

