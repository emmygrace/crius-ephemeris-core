Type Definitions
=================

This module contains all type definitions for ephemeris calculations.

EphemerisSettings
-----------------

.. autoclass:: crius_ephemeris_core.types.EphemerisSettings
   :members:
   :undoc-members:
   :show-inheritance:

EphemerisSettings defines the configuration for ephemeris calculations.

**Required Fields:**

* ``zodiac_type``: Literal["tropical", "sidereal"] - The zodiac type to use
* ``ayanamsa``: Optional[str] - Ayanamsa for sidereal calculations (e.g., "lahiri")
* ``house_system``: str - House system name (e.g., "placidus", "whole_sign")
* ``include_objects``: list[str] - List of celestial objects to include

**Optional Fields:**

* ``vedic_options``: VedicOptions - Optional Vedic/Jyotish configuration

Example:

.. code-block:: python

   settings: EphemerisSettings = {
       "zodiac_type": "tropical",
       "ayanamsa": None,
       "house_system": "placidus",
       "include_objects": ["sun", "moon", "mercury", "venus", "mars"],
   }

GeoLocation
-----------

.. autoclass:: crius_ephemeris_core.types.GeoLocation
   :members:
   :undoc-members:
   :show-inheritance:

GeoLocation represents a geographic location with latitude and longitude.

**Required Fields:**

* ``lat``: float - Latitude in degrees (-90 to 90)
* ``lon``: float - Longitude in degrees (-180 to 180)

Example:

.. code-block:: python

   location: GeoLocation = {
       "lat": 40.7128,  # New York
       "lon": -74.0060,
   }

PlanetPosition
--------------

.. autoclass:: crius_ephemeris_core.types.PlanetPosition
   :members:
   :undoc-members:
   :show-inheritance:

PlanetPosition represents the position of a celestial object.

**Required Fields:**

* ``lon``: float - Longitude in degrees (0-360)
* ``lat``: float - Latitude in degrees
* ``speed_lon``: float - Speed in longitude (degrees per day)
* ``retrograde``: bool - Whether the planet is retrograde

HousePositions
-------------

.. autoclass:: crius_ephemeris_core.types.HousePositions
   :members:
   :undoc-members:
   :show-inheritance:

HousePositions represents house system positions.

**Required Fields:**

* ``system``: str - House system name
* ``cusps``: dict[str, float] - House cusps: "1".."12" -> degrees
* ``angles``: dict[str, float] - Angles: "asc", "mc", "ic", "dc" -> degrees

LayerPositions
--------------

.. autoclass:: crius_ephemeris_core.types.LayerPositions
   :members:
   :undoc-members:
   :show-inheritance:

LayerPositions contains complete position data for a chart layer.

**Required Fields:**

* ``planets``: dict[str, PlanetPosition] - Planet ID -> position
* ``houses``: Optional[HousePositions] - House positions (None if no location provided)

LayerContext
------------

.. autoclass:: crius_ephemeris_core.types.LayerContext
   :members:
   :undoc-members:
   :show-inheritance:

LayerContext provides context for calculating positions for a chart layer.

**Required Fields:**

* ``layer_id``: str - Layer identifier
* ``kind``: str - Layer kind (e.g., "natal", "transit", "progressed")
* ``datetime``: datetime - UTC datetime for calculation
* ``location``: Optional[GeoLocation] - Geographic location
* ``settings``: EphemerisSettings - Ephemeris calculation settings

VedicOptions
------------

.. autoclass:: crius_ephemeris_core.types.VedicOptions
   :members:
   :undoc-members:
   :show-inheritance:

VedicOptions provides optional configuration flags for Vedic/Jyotish calculations.

All fields are optional:

* ``include_nakshatras``: bool - Include nakshatra information
* ``enabled_vargas``: List[str] - List of divisional charts to calculate
* ``include_dashas``: bool - Include dasha timelines
* ``dasha_systems``: List[str] - Dasha systems to use
* ``dashas_depth``: Literal["mahadasha", "antardasha", "pratyantardasha"] - Dasha depth
* ``include_yogas``: bool - Include yoga detection

