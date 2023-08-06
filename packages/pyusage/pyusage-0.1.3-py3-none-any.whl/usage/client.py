from __future__ import annotations

from typing import Set

from .models import Session


def send(session: Session) -> None:
    """Do something."""
    print("post:", session)
