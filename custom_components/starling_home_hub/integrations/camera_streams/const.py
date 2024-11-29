"""Constants for the Camera Streams integration."""

from datetime import timedelta
from pathlib import Path

PLACEHOLDER = Path(__file__).parent / "placeholder.png"
STREAM_EXPIRATION_BUFFER = timedelta(seconds=60)
