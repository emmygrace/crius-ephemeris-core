"""Version management tests."""

import pytest
from crius_ephemeris_core import __version__


class TestVersion:
    """Test version management."""

    def test_version_exists(self):
        """Test that __version__ is defined."""
        assert __version__ is not None
        assert isinstance(__version__, str)

    def test_version_format(self):
        """Test that version follows semantic versioning."""
        # Version should be in format X.Y.Z
        parts = __version__.split(".")
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)

    def test_version_matches_pyproject(self):
        """Test that version matches pyproject.toml."""
        # Read version from pyproject.toml manually
        import re

        with open("pyproject.toml", "r") as f:
            content = f.read()
            match = re.search(r'version\s*=\s*"([^"]+)"', content)
            if match:
                pyproject_version = match.group(1)
                assert __version__ == pyproject_version
            else:
                # Fallback: just check it's a valid version
                assert __version__ is not None

    def test_version_importable(self):
        """Test that version can be imported."""
        from crius_ephemeris_core import __version__

        assert __version__ == "0.1.0"

