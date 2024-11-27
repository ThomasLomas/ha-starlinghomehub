"""Models for handling WebRTC stream."""
from dataclasses import dataclass


@dataclass
class StartStream:
    """Class for handling starting a WebRTC stream."""

    status: str
    answer: str
    streamId: str
    isLocal: bool


@dataclass
class StreamStatus:
    """Class for stream status."""

    status: str


@dataclass
class StreamExtend:
    """Class for extending stream."""

    status: str
