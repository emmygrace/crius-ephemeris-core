Basic Usage Examples
=====================

This page provides basic usage examples for the crius-ephemeris-core package.

Defining Settings
-----------------

.. code-block:: python

   from crius_ephemeris_core import EphemerisSettings

   # Tropical zodiac settings
   tropical_settings: EphemerisSettings = {
       "zodiac_type": "tropical",
       "ayanamsa": None,
       "house_system": "placidus",
       "include_objects": ["sun", "moon", "mercury", "venus", "mars"],
   }

   # Sidereal zodiac settings
   sidereal_settings: EphemerisSettings = {
       "zodiac_type": "sidereal",
       "ayanamsa": "lahiri",
       "house_system": "whole_sign",
       "include_objects": ["sun", "moon", "mercury", "venus", "mars"],
   }

   # With Vedic options
   vedic_settings: EphemerisSettings = {
       "zodiac_type": "sidereal",
       "ayanamsa": "lahiri",
       "house_system": "whole_sign",
       "include_objects": ["sun", "moon", "mercury", "venus", "mars"],
       "vedic_options": {
           "include_nakshatras": True,
           "enabled_vargas": ["d9", "d10"],
           "include_dashas": True,
           "dasha_systems": ["vimshottari"],
           "dashas_depth": "pratyantardasha",
       },
   }

Defining Locations
------------------

.. code-block:: python

   from crius_ephemeris_core import GeoLocation

   # New York
   ny_location: GeoLocation = {
       "lat": 40.7128,
       "lon": -74.0060,
   }

   # London
   london_location: GeoLocation = {
       "lat": 51.5074,
       "lon": -0.1278,
   }

   # Tokyo
   tokyo_location: GeoLocation = {
       "lat": 35.6762,
       "lon": 139.6503,
   }

Working with Positions
----------------------

.. code-block:: python

   from crius_ephemeris_core import PlanetPosition, HousePositions, LayerPositions

   # Planet position
   sun_position: PlanetPosition = {
       "lon": 280.5,  # Capricorn
       "lat": 0.0,
       "speed_lon": 1.0,
       "retrograde": False,
   }

   # House positions
   houses: HousePositions = {
       "system": "placidus",
       "cusps": {
           "1": 15.0,
           "2": 45.0,
           "3": 75.0,
           # ... houses 4-12 ...
       },
       "angles": {
           "asc": 15.0,
           "mc": 105.0,
           "ic": 285.0,
           "dc": 195.0,
       },
   }

   # Complete layer positions
   layer_positions: LayerPositions = {
       "planets": {
           "sun": sun_position,
           "moon": {
               "lon": 45.2,
               "lat": 2.1,
               "speed_lon": 13.0,
               "retrograde": False,
           },
       },
       "houses": houses,
   }

Creating Layer Context
----------------------

.. code-block:: python

   from datetime import datetime, timezone
   from crius_ephemeris_core import LayerContext, EphemerisSettings, GeoLocation

   # Create a layer context for a natal chart
   natal_context: LayerContext = {
       "layer_id": "natal",
       "kind": "natal",
       "datetime": datetime(1990, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
       "location": {
           "lat": 40.7128,
           "lon": -74.0060,
       },
       "settings": {
           "zodiac_type": "tropical",
           "ayanamsa": None,
           "house_system": "placidus",
           "include_objects": ["sun", "moon", "mercury", "venus", "mars"],
       },
   }

   # Create a layer context for a transit (no location needed)
   transit_context: LayerContext = {
       "layer_id": "transit",
       "kind": "transit",
       "datetime": datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
       "location": None,
       "settings": {
           "zodiac_type": "tropical",
           "ayanamsa": None,
           "house_system": "placidus",
           "include_objects": ["sun", "moon"],
       },
   }

Type Checking
-------------

The package uses TypedDict for type safety. You can use type checkers like mypy to validate your code:

.. code-block:: python

   # This will be caught by type checkers
   invalid_settings: EphemerisSettings = {
       "zodiac_type": "invalid",  # Error: not a valid literal
       "ayanamsa": None,
       "house_system": "placidus",
       "include_objects": [],
   }

   # This is valid
   valid_settings: EphemerisSettings = {
       "zodiac_type": "tropical",  # Valid literal
       "ayanamsa": None,
       "house_system": "placidus",
       "include_objects": [],
   }

