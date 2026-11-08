"""TLOW — modular AI assistant backend with composable intelligence primitives."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

from tlow.sdk import TLOW, MemoryHandle, SystemBuilder, TLOWSystem

try:
    __version__ = _pkg_version("tlow")
except PackageNotFoundError:  # pragma: no cover — uninstalled source tree
    __version__ = "0.0.0+unknown"

__all__ = ["TLOW", "TLOWSystem", "MemoryHandle", "SystemBuilder", "__version__"]
