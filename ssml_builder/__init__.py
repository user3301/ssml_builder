"""
SSML Builder - A utility class for building Speech Synthesis Markup Language (SSML).

This package provides a fluent interface for building SSML text for use with
text-to-speech services like Amazon Polly, Google TTS, and Microsoft Watson.
"""

from ssml_builder.builder import Speech

__version__: str = "1.0.0"
__all__: list[str] = ["Speech"]
