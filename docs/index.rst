crius-ephemeris-core Documentation
==================================

**Crius** - Core ephemeris types and interfaces for astrological calculations.

Named after `Crius <https://en.wikipedia.org/wiki/Crius>`_, the Titan of constellations and measuring the year in Greek mythology.

Overview
--------

This package provides pure abstractions for ephemeris calculations:

* Type definitions for ephemeris data structures
* Protocol/interface definitions for ephemeris adapters
* Core service interfaces (without database dependencies)

**No external dependencies** - This package is MIT licensed and contains only pure Python types and interfaces.

Contents
--------

.. toctree::
   :maxdepth: 2

   api/types
   api/protocols
   examples/basic_usage
   examples/adapter_implementation

Installation
------------

.. code-block:: bash

   pip install crius-ephemeris-core

Or for development:

.. code-block:: bash

   pip install -e packages/crius-ephemeris-core

Quick Start
-----------

.. code-block:: python

   from crius_ephemeris_core import (
       EphemerisSettings,
       GeoLocation,
       PlanetPosition,
       HousePositions,
       LayerPositions,
       LayerContext,
   )

   # Define ephemeris settings
   settings: EphemerisSettings = {
       "zodiac_type": "tropical",
       "ayanamsa": None,
       "house_system": "placidus",
       "include_objects": ["sun", "moon", "mercury"],
   }

   # Define location
   location: GeoLocation = {
       "lat": 40.7128,
       "lon": -74.0060,
   }

License
-------

MIT License - This package contains no Swiss Ephemeris code or dependencies.

Related Packages
----------------

* ``crius-swiss`` - Swiss Ephemeris adapter implementation (AGPL/LGPL licensed)

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

