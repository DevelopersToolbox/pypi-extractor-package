"""
This module initializes the PyPI package info retriever and handles package metadata.

Attributes:
- __version__: The version of the package, retrieved from the package metadata.
- __all__: A list of all public symbols that the module exports.
"""

import importlib.metadata

from .exceptions import PyPiExtractorError
from .pypi import PyPiExtractor

try:
    __version__: str = importlib.metadata.version('pypi_extractor')
except importlib.metadata.PackageNotFoundError:
    __version__ = 'unknown'

__all__: list[str] = [
    'PyPiExtractorError',
    'PyPiExtractor'
]
