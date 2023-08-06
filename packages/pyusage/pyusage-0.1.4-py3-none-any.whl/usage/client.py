from __future__ import annotations

from .models import Session


def send(session: Session) -> None:
    """Do something."""
    print("post:", session)
