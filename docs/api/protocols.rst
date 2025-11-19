Protocol Definitions
===================

This module defines the protocol interface that ephemeris adapter implementations must conform to.

EphemerisAdapter
----------------

.. autoclass:: crius_ephemeris_core.protocols.EphemerisAdapter
   :members:
   :undoc-members:
   :show-inheritance:

EphemerisAdapter is a Protocol that defines the interface for ephemeris calculation adapters.

Implementations of this protocol provide ephemeris calculations using various underlying libraries (Swiss Ephemeris, JPL, etc.).

Method: calc_positions
~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: crius_ephemeris_core.protocols.EphemerisAdapter.calc_positions

Calculate planetary and house positions for a given datetime and location.

**Parameters:**

* ``dt_utc`` (datetime): UTC datetime for the calculation
* ``location`` (Optional[GeoLocation]): Optional geographic location (required for house calculations)
* ``settings`` (EphemerisSettings): Ephemeris calculation settings

**Returns:**

* ``LayerPositions``: Contains planetary positions and optionally house positions

**Raises:**

* Various exceptions depending on implementation (e.g., if ephemeris data is missing or calculation fails)

Example Implementation
-----------------------

Here's a minimal example of implementing the EphemerisAdapter protocol:

.. code-block:: python

   from datetime import datetime
   from typing import Optional
   from crius_ephemeris_core import (
       EphemerisAdapter,
       EphemerisSettings,
       GeoLocation,
       LayerPositions,
       PlanetPosition,
   )

   class MyEphemerisAdapter:
       """Custom ephemeris adapter implementation."""

       def calc_positions(
           self,
           dt_utc: datetime,
           location: Optional[GeoLocation],
           settings: EphemerisSettings,
       ) -> LayerPositions:
           # Your implementation here
           planets: dict[str, PlanetPosition] = {}
           # ... calculate positions ...

           return {
               "planets": planets,
               "houses": None,  # Or calculate houses if location provided
           }

   # The adapter automatically conforms to the protocol
   adapter: EphemerisAdapter = MyEphemerisAdapter()

Conformance Testing
-------------------

Use the testing utilities in ``crius_ephemeris_core.testing`` to verify your adapter implementation conforms to the protocol.

See :doc:`../examples/adapter_implementation` for more details.

