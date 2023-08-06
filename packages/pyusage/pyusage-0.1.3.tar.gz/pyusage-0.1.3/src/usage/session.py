from __future__ import annotations

import atexit
from typing import TYPE_CHECKING, Dict, Optional, Set

from . import client, models

if TYPE_CHECKING:
    from .wrapped_function import WrappedFunction

__all__ = ["init", "shutdown"]

_session = None  # pylint: disable=invalid-name


def is_initialized() -> bool:
    """Do something."""
    return _session is not None


def init(session: Optional[Session] = None) -> None:
    """Initialize PyUsage.

    Arguments:
        session: .
    """
    global _session  # pylint: disable=invalid-name, global-statement
    if session is None:
        _session = Session()
    else:
        _session = session


def shutdown() -> None:
    """Do something."""
    global _session  # pylint: disable=invalid-name, global-statement
    if not is_initialized():
        return

    client.send(_session.model)
    _session = None


atexit.register(shutdown)


def get_current_session() -> Session:
    """Do something."""
    if not is_initialized():
        init()

    assert _session is not None
    return _session


class Session:
    """Is something."""

    def __init__(self):
        """Do something."""
        self._metadata = None
        self._functions = set()

    @property
    def metadata(self) -> Optional[Dict[str, str]]:
        """Do something."""
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: Dict[str, str]) -> None:
        """Do something."""
        assert self._metadata is None
        self._metadata = metadata

    @property
    def functions(self) -> Set[WrappedFunction]:
        """Do something."""
        return self._functions

    @property
    def model(self) -> models.Session:
        """Do something."""
        return models.Session(
            uid="adsf",
            metadata=self.metadata,
            functions=list(function.model for function in self._functions),
        )

    def register(self, function: WrappedFunction) -> None:
        """Do something."""
        self._functions.add(function)
