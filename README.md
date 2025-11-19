# crius-ephemeris-core

**Crius** - Core ephemeris types and interfaces for astrological calculations.

Named after [Crius](https://en.wikipedia.org/wiki/Crius), the Titan of constellations and measuring the year in Greek mythology.

## Overview

This package provides pure abstractions for ephemeris calculations:
- Type definitions for ephemeris data structures
- Protocol/interface definitions for ephemeris adapters
- Core service interfaces (without database dependencies)

**No external dependencies** - This package is MIT licensed and contains only pure Python types and interfaces.

## Installation

```bash
pip install crius-ephemeris-core
```

Or for development:

```bash
pip install -e packages/crius-ephemeris-core
```

## Usage

### Types

```python
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
```

### Adapter Protocol

```python
from crius_ephemeris_core import EphemerisAdapter, LayerPositions
from datetime import datetime

# Use the protocol to define your own adapter
class MyEphemerisAdapter:
    def calc_positions(
        self,
        dt_utc: datetime,
        location: Optional[GeoLocation],
        settings: EphemerisSettings,
    ) -> LayerPositions:
        # Your implementation
        ...
```

## Package Structure

- `crius_ephemeris_core/types.py` - All type definitions
- `crius_ephemeris_core/protocols.py` - Adapter protocol definitions
- `crius_ephemeris_core/service.py` - Core service interfaces (optional, cache-free)

## Documentation

Full API documentation is available in the `docs/` directory. To build the documentation:

```bash
# Install documentation dependencies
pip install sphinx sphinx-rtd-theme

# Build documentation
cd docs
make html
```

The documentation will be generated in `docs/_build/html/`.

## License

MIT License - This package contains no Swiss Ephemeris code or dependencies.

## Related Packages

- `crius-swiss` - Swiss Ephemeris adapter implementation (AGPL/LGPL licensed)

