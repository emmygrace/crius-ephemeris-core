"""
Protocol testing utilities for verifying adapter implementations.

This module provides utilities to test that adapter implementations conform
to the EphemerisAdapter protocol.
"""

import inspect
from datetime import datetime
from typing import Optional, List, Dict, Any, Type
from typing import get_type_hints, get_origin, get_args

from .protocols import EphemerisAdapter
from .types import (
    EphemerisSettings,
    GeoLocation,
    LayerPositions,
    PlanetPosition,
    HousePositions,
)


class ProtocolConformanceError(Exception):
    """Raised when an adapter does not conform to the protocol."""

    def __init__(self, message: str, errors: List[str]):
        super().__init__(message)
        self.errors = errors


def verify_adapter_protocol(adapter: Any) -> List[str]:
    """
    Verify that an adapter conforms to the EphemerisAdapter protocol.

    Args:
        adapter: Adapter instance to verify

    Returns:
        List of error messages (empty if conformant)

    Example:
        >>> errors = verify_adapter_protocol(my_adapter)
        >>> if errors:
        ...     print("Protocol errors:", errors)
    """
    errors: List[str] = []

    # Check that adapter has calc_positions method
    if not hasattr(adapter, "calc_positions"):
        errors.append("Adapter must have 'calc_positions' method")
        return errors

    method = getattr(adapter, "calc_positions")

    # Check method signature
    try:
        sig = inspect.signature(method)
        params = list(sig.parameters.keys())

        # Check required parameters
        if "dt_utc" not in params:
            errors.append("calc_positions must have 'dt_utc' parameter")
        if "location" not in params:
            errors.append("calc_positions must have 'location' parameter")
        if "settings" not in params:
            errors.append("calc_positions must have 'settings' parameter")

        # Check parameter types (if annotations are available)
        annotations = get_type_hints(method)
        if "dt_utc" in annotations:
            if annotations["dt_utc"] != datetime:
                errors.append(
                    f"calc_positions 'dt_utc' parameter must be datetime, "
                    f"got {annotations['dt_utc']}"
                )
        if "location" in annotations:
            location_type = annotations["location"]
            if get_origin(location_type) is not Optional:
                args = get_args(location_type)
                if GeoLocation not in args:
                    errors.append(
                        f"calc_positions 'location' parameter must be "
                        f"Optional[GeoLocation], got {location_type}"
                    )
        if "settings" in annotations:
            if annotations["settings"] != EphemerisSettings:
                errors.append(
                    f"calc_positions 'settings' parameter must be "
                    f"EphemerisSettings, got {annotations['settings']}"
                )

        # Check return type
        if "return" in annotations:
            if annotations["return"] != LayerPositions:
                errors.append(
                    f"calc_positions must return LayerPositions, "
                    f"got {annotations['return']}"
                )

    except Exception as e:
        errors.append(f"Error checking method signature: {e}")

    return errors


def verify_adapter_runtime(
    adapter: Any,
    dt_utc: Optional[datetime] = None,
    location: Optional[GeoLocation] = None,
    settings: Optional[EphemerisSettings] = None,
) -> List[str]:
    """
    Verify adapter at runtime by calling calc_positions.

    Args:
        adapter: Adapter instance to verify
        dt_utc: Optional datetime for test (defaults to current time)
        location: Optional location for test
        settings: Optional settings for test (defaults to minimal settings)

    Returns:
        List of error messages (empty if conformant)

    Example:
        >>> errors = verify_adapter_runtime(my_adapter)
        >>> if errors:
        ...     print("Runtime errors:", errors)
    """
    errors: List[str] = []

    if dt_utc is None:
        dt_utc = datetime.now()

    if settings is None:
        settings = {
            "zodiac_type": "tropical",
            "ayanamsa": None,
            "house_system": "placidus",
            "include_objects": ["sun"],
        }

    try:
        # Call the method
        result = adapter.calc_positions(dt_utc, location, settings)

        # Verify return type structure
        if not isinstance(result, dict):
            errors.append("calc_positions must return a dict")
            return errors

        # Check required keys
        if "planets" not in result:
            errors.append("Return value must have 'planets' key")
        if "houses" not in result:
            errors.append("Return value must have 'houses' key")

        # Verify planets structure
        if "planets" in result:
            planets = result["planets"]
            if not isinstance(planets, dict):
                errors.append("'planets' must be a dict")
            else:
                for planet_id, position in planets.items():
                    if not isinstance(planet_id, str):
                        errors.append(f"Planet IDs must be strings, got {type(planet_id)}")
                    if not isinstance(position, dict):
                        errors.append(f"Planet positions must be dicts, got {type(position)}")
                    else:
                        required_fields = ["lon", "lat", "speed_lon", "retrograde"]
                        for field in required_fields:
                            if field not in position:
                                errors.append(
                                    f"Planet position must have '{field}' field"
                                )

        # Verify houses structure (if present)
        if "houses" in result and result["houses"] is not None:
            houses = result["houses"]
            if not isinstance(houses, dict):
                errors.append("'houses' must be a dict or None")
            else:
                required_fields = ["system", "cusps", "angles"]
                for field in required_fields:
                    if field not in houses:
                        errors.append(f"House positions must have '{field}' field")

    except Exception as e:
        errors.append(f"Runtime error calling calc_positions: {e}")

    return errors


class MockEphemerisAdapter:
    """
    Mock adapter for testing.

    Implements EphemerisAdapter protocol with configurable behavior.
    """

    def __init__(
        self,
        return_value: Optional[LayerPositions] = None,
        raise_error: Optional[Exception] = None,
    ):
        """
        Initialize mock adapter.

        Args:
            return_value: Value to return from calc_positions
            raise_error: Exception to raise (if any)
        """
        self.return_value = return_value or {
            "planets": {},
            "houses": None,
        }
        self.raise_error = raise_error
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
        if self.raise_error:
            raise self.raise_error

        self.call_count += 1
        self.last_dt = dt_utc
        self.last_location = location
        self.last_settings = settings

        return self.return_value


def create_test_adapter(
    planets: Optional[Dict[str, PlanetPosition]] = None,
    houses: Optional[HousePositions] = None,
) -> MockEphemerisAdapter:
    """
    Create a test adapter with specified return values.

    Args:
        planets: Optional dict of planet positions
        houses: Optional house positions

    Returns:
        MockEphemerisAdapter instance

    Example:
        >>> adapter = create_test_adapter(
        ...     planets={"sun": {"lon": 280.5, "lat": 0.0, "speed_lon": 1.0, "retrograde": False}},
        ...     houses={"system": "placidus", "cusps": {}, "angles": {}}
        ... )
    """
    return_value: LayerPositions = {
        "planets": planets or {},
        "houses": houses,
    }
    return MockEphemerisAdapter(return_value=return_value)

