Adapter Implementation Guide
============================

This guide shows how to implement an ephemeris adapter that conforms to the ``EphemerisAdapter`` protocol.

Basic Implementation
--------------------

Here's a minimal adapter implementation:

.. code-block:: python

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

   class SimpleEphemerisAdapter:
       """A simple ephemeris adapter implementation."""

       def calc_positions(
           self,
           dt_utc: datetime,
           location: Optional[GeoLocation],
           settings: EphemerisSettings,
       ) -> LayerPositions:
           """
           Calculate planetary and house positions.

           This is a minimal implementation that returns mock data.
           In a real implementation, you would use an ephemeris library
           like Swiss Ephemeris or JPL.
           """
           # Extract settings
           include_objects = settings.get("include_objects", [])

           # Calculate planet positions
           planets: dict[str, PlanetPosition] = {}
           for obj_id in include_objects:
               # In a real implementation, calculate actual positions
               planets[obj_id] = {
                   "lon": 0.0,
                   "lat": 0.0,
                   "speed_lon": 1.0,
                   "retrograde": False,
               }

           # Calculate houses if location is provided
           houses: Optional[HousePositions] = None
           if location:
               houses = {
                   "system": settings["house_system"],
                   "cusps": {str(i): 0.0 for i in range(1, 13)},
                   "angles": {
                       "asc": 0.0,
                       "mc": 0.0,
                       "ic": 180.0,
                       "dc": 180.0,
                   },
               }

           return {
               "planets": planets,
               "houses": houses,
           }

   # The adapter automatically conforms to the protocol
   adapter: EphemerisAdapter = SimpleEphemerisAdapter()

Using the Adapter
-----------------

Once you've implemented an adapter, you can use it like any other adapter:

.. code-block:: python

   from datetime import datetime, timezone

   adapter = SimpleEphemerisAdapter()

   settings: EphemerisSettings = {
       "zodiac_type": "tropical",
       "ayanamsa": None,
       "house_system": "placidus",
       "include_objects": ["sun", "moon"],
   }

   location: GeoLocation = {
       "lat": 40.7128,
       "lon": -74.0060,
   }

   dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

   positions = adapter.calc_positions(dt, location, settings)

   print(positions["planets"]["sun"])
   print(positions["houses"])

Verifying Protocol Conformance
------------------------------

You can use the testing utilities to verify your adapter conforms to the protocol:

.. code-block:: python

   from crius_ephemeris_core.testing import verify_adapter_protocol

   adapter = SimpleEphemerisAdapter()

   # Verify the adapter conforms to the protocol
   errors = verify_adapter_protocol(adapter)
   if errors:
       print("Protocol conformance errors:", errors)
   else:
       print("Adapter conforms to protocol!")

Best Practices
--------------

1. **Handle Missing Data Gracefully**: If an ephemeris library doesn't support a particular object, skip it rather than failing.

2. **Validate Inputs**: Check that settings and locations are valid before performing calculations.

3. **Handle Optional Location**: The location parameter is optional. If None, you should return houses as None.

4. **Normalize Longitudes**: Ensure longitudes are in the 0-360 degree range.

5. **Support All House Systems**: If possible, support multiple house systems as specified in settings.

6. **Error Handling**: Raise appropriate exceptions if calculations fail, with helpful error messages.

7. **Thread Safety**: Document whether your adapter is thread-safe if it will be used in concurrent environments.

Example: Swiss Ephemeris Adapter
----------------------------------

For a real-world example, see the ``crius-swiss`` package, which implements the protocol using Swiss Ephemeris.

Example: JPL Ephemeris Adapter
--------------------------------

For another example, see the ``crius-jpl`` package, which implements the protocol using NASA JPL DE430t ephemeris data.

