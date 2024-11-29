"""Models for the status response from the Starling Home Hub API."""

from dataclasses import dataclass, fields


@dataclass
class Permissions:
    """Class that reflects permissions response."""

    read: bool
    write: bool
    camera: bool


@dataclass
class Status:
    """Class that reflects a status response."""

    apiVersion: float
    apiReady: bool
    appName: str
    permissions: Permissions

    @classmethod
    def create_from_dict(cls, dict_):
        """Create a Status from a dict."""
        class_fields = {f.name for f in fields(cls)}
        return Status(**{k: v for k, v in dict_.items() if k in class_fields})
