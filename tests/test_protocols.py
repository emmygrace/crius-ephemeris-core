"""Protocol conformance tests."""

import pytest
from datetime import datetime
from typing import Optional

from crius_ephemeris_core import (
    EphemerisAdapter,
    EphemerisSettings,
    GeoLocation,
    LayerPositions,
    PlanetPosition,
    HousePositions,
)


class MockEphemerisAdapter:
    """Mock adapter implementing EphemerisAdapter protocol."""

    def __init__(self, return_value: LayerPositions):
        """Initialize with a return value."""
        self.return_value = return_value
        self.call_count = 0
        self.last_dt: Optional[datetime] = None
        self.last_location: Optional[GeoLocation] = None
        self.last_settings: Optional[EphemerisSettings] = None

    def calc_positions(
        self,
        dt_utc: datetime,
        location: Optional[GeoLocation],
        settings: EphemerisSettings,
    ) -> LayerPositions:
        """Calculate positions (mock implementation)."""
        self.call_count += 1
        self.last_dt = dt_utc
        self.last_location = location
        self.last_settings = settings
        return self.return_value


class TestEphemerisAdapterProtocol:
    """Test EphemerisAdapter protocol conformance."""

    def test_protocol_has_calc_positions_method(self):
        """Test that protocol defines calc_positions method."""
        # Check that EphemerisAdapter is a Protocol
        from typing import Protocol

        assert issubclass(EphemerisAdapter, Protocol)

    def test_mock_adapter_conforms_to_protocol(self):
        """Test that MockEphemerisAdapter conforms to protocol."""
        mock_return: LayerPositions = {
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

        adapter = MockEphemerisAdapter(mock_return)
        assert isinstance(adapter, EphemerisAdapter)

    def test_protocol_method_signature(self):
        """Test that protocol method has correct signature."""
        import inspect

        # Get the protocol method signature
        sig = inspect.signature(EphemerisAdapter.calc_positions)
        params = list(sig.parameters.keys())

        # Should have dt_utc, location, settings
        assert "dt_utc" in params
        assert "location" in params
        assert "settings" in params

        # Check parameter types
        annotations = sig.parameters
        assert annotations["dt_utc"].annotation == datetime
        assert annotations["location"].annotation == Optional[GeoLocation]
        assert annotations["settings"].annotation == EphemerisSettings

        # Check return type
        assert sig.return_annotation == LayerPositions

    def test_adapter_can_be_used_polymorphically(self):
        """Test that adapters can be used through protocol interface."""
        mock_return: LayerPositions = {
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

        adapter: EphemerisAdapter = MockEphemerisAdapter(mock_return)

        dt = datetime(2024, 1, 1, 12, 0, 0)
        settings: EphemerisSettings = {
            "zodiac_type": "tropical",
            "ayanamsa": None,
            "house_system": "placidus",
            "include_objects": ["sun"],
        }
        location: Optional[GeoLocation] = {"lat": 40.7128, "lon": -74.0060}

        result = adapter.calc_positions(dt, location, settings)

        assert result == mock_return
        assert isinstance(result, dict)
        assert "planets" in result
        assert "houses" in result

    def test_return_type_validation(self):
        """Test that return type matches LayerPositions structure."""
        mock_return: LayerPositions = {
            "planets": {
                "sun": {
                    "lon": 280.5,
                    "lat": 0.0,
                    "speed_lon": 1.0,
                    "retrograde": False,
                },
                "moon": {
                    "lon": 45.2,
                    "lat": 2.1,
                    "speed_lon": 13.0,
                    "retrograde": False,
                },
            },
            "houses": {
                "system": "placidus",
                "cusps": {"1": 15.0, "2": 45.0},
                "angles": {"asc": 15.0, "mc": 105.0, "ic": 285.0, "dc": 195.0},
            },
        }

        adapter = MockEphemerisAdapter(mock_return)
        dt = datetime(2024, 1, 1, 12, 0, 0)
        settings: EphemerisSettings = {
            "zodiac_type": "tropical",
            "ayanamsa": None,
            "house_system": "placidus",
            "include_objects": ["sun", "moon"],
        }

        result = adapter.calc_positions(dt, None, settings)

        # Validate structure
        assert isinstance(result, dict)
        assert "planets" in result
        assert "houses" in result
        assert isinstance(result["planets"], dict)
        assert isinstance(result["houses"], dict) or result["houses"] is None

        # Validate planet positions
        for planet_id, position in result["planets"].items():
            assert isinstance(planet_id, str)
            assert "lon" in position
            assert "lat" in position
            assert "speed_lon" in position
            assert "retrograde" in position
            assert isinstance(position["lon"], (int, float))
            assert isinstance(position["lat"], (int, float))
            assert isinstance(position["speed_lon"], (int, float))
            assert isinstance(position["retrograde"], bool)

        # Validate houses if present
        if result["houses"] is not None:
            houses = result["houses"]
            assert "system" in houses
            assert "cusps" in houses
            assert "angles" in houses
            assert isinstance(houses["system"], str)
            assert isinstance(houses["cusps"], dict)
            assert isinstance(houses["angles"], dict)

    def test_adapter_with_none_location(self):
        """Test that adapter can handle None location."""
        mock_return: LayerPositions = {
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

        adapter = MockEphemerisAdapter(mock_return)
        dt = datetime(2024, 1, 1, 12, 0, 0)
        settings: EphemerisSettings = {
            "zodiac_type": "tropical",
            "ayanamsa": None,
            "house_system": "placidus",
            "include_objects": ["sun"],
        }

        result = adapter.calc_positions(dt, None, settings)

        assert result["houses"] is None
        assert adapter.last_location is None

