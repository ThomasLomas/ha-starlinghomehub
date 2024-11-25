"""Models used by Starling Home Hub."""

from dataclasses import dataclass

@dataclass
class Device:
    """Class that reflects a device."""

    type: str
    id: str
    where: str
    name: str
    serialNumber: str
    structureName: str

    # Protect
    smokeDetected: bool
    coDetected: bool
    batteryStatus: str
    manualTestActive: bool
    smokeStateDetail: str
    coStateDetail: str
    occupancyDetected: bool

    # Camera
    supportsStreaming: bool
    cameraModel: str

@dataclass
class Permissions:
    """Class that reflects permissions response."""

    read: bool
    write: bool
    camera: bool


@dataclass
class Devices:
    """Class that reflects a devices response."""

    status: bool
    devices: list[Device]

@dataclass
class SpecificDevice:
    """Class that reflects a specific device."""

    status: str
    properties: Device

@dataclass
class Status:
    """Class that reflects a status response."""

    apiVersion: float
    apiReady: bool
    connectedToGoogleHome: bool
    appName: str
    permissions: Permissions

@dataclass
class CoordinatorData:
    """Class that houses all the coordinator data required."""

    devices: dict[str, SpecificDevice]
    status: Status

@dataclass
class StartStream:
    """Class for handling starting a WebRTC stream."""

    status: str
    answer: str
    streamId: str

@dataclass
class StreamStatus:
    """Class for stream status."""

    status: str
