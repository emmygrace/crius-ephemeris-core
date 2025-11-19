# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-01

### Added
- Initial release of crius-ephemeris-core
- Type definitions for ephemeris data structures:
  - `EphemerisSettings` - Configuration for ephemeris calculations
  - `GeoLocation` - Geographic location coordinates
  - `PlanetPosition` - Planetary position data
  - `HousePositions` - House system positions
  - `LayerPositions` - Complete position data for a chart layer
  - `LayerContext` - Context for calculating positions
  - `VedicOptions` - Optional Vedic/Jyotish configuration
- Protocol definitions:
  - `EphemerisAdapter` - Protocol for ephemeris calculation adapters
- Service interfaces:
  - `EphemerisService` - Abstract base class for ephemeris services
  - `BaseEphemerisService` - Base implementation with adapter delegation
  - `CachedEphemerisService` - Service with caching support
  - `CacheProvider` - Protocol for cache providers
  - `create_ephemeris_service()` - Factory function for creating services
- Runtime validation (optional):
  - Pydantic-based validation models
  - `validate_ephemeris_settings()` - Validate EphemerisSettings
  - `validate_geo_location()` - Validate GeoLocation
  - `validate_layer_positions()` - Validate LayerPositions
  - `validate_layer_context()` - Validate LayerContext
  - `validate_planet_position()` - Validate PlanetPosition
  - `validate_house_positions()` - Validate HousePositions
- Testing utilities:
  - `verify_adapter_protocol()` - Verify adapter protocol conformance
  - `verify_adapter_runtime()` - Runtime verification of adapters
  - `MockEphemerisAdapter` - Mock adapter for testing
  - `create_test_adapter()` - Factory for test adapters
- Documentation:
  - Sphinx documentation with API reference
  - Usage examples and guides
  - Adapter implementation guide
- Test suite:
  - Unit tests for type definitions
  - Protocol conformance tests
  - Version management tests

[0.1.0]: https://github.com/gaia-tools/crius-ephemeris-core/releases/tag/v0.1.0

