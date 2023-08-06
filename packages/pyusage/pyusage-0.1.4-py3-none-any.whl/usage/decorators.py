import functools
from typing import Callable, Dict, List, Optional

from .session import get_current_session
from .wrapped_function import WrappedFunction

__all__ = ["metadata", "collect"]


def metadata(function: Callable[[], Dict[str, str]]):
    """Specify metadata about the session.

    Examples:
        >>> import platform
        >>> import usage
        >>>
        >>> __version__ = "0.27.3"
        >>>
        >>> @usage.metadata
        >>> def get_metadata():
        ...     return {
        ...         "Python": platform.python_version(),
        ...         "OS": platform.system(),
        ...         "Version": __version__
        ...     }

    Raises:
        RuntimeError: If foo
    """
    session = get_current_session()
    if session.metadata is not None:
        raise RuntimeError
    session.metadata = function()
    return function


def collect(
    function: Optional[Callable] = None,
    *,
    labels: Optional[List[str]] = None,
    secrets: Optional[List[str]] = None,
):
    """Collect usage data from a function.

    Arguments:
        function: The function you want to collect usage data on.
        labels: A list of strings you'd like to label this function with.
        secrets: The names of parameters that are sensitive.

    Examples:
        Aasdf

        >>> import usage
        >>>
        >>> @usage.collect(secrets=["token"])
        ... def login(token: str):
        ...     ...

        asdf

        >>> import usage
        >>>
        >>> @usage.collect(labels=["foo"])
        ... def foo():
        ...     ...


    """

    def wrap(function):
        session = get_current_session()
        wrapped_function = WrappedFunction(function, labels, secrets)
        session.register(wrapped_function)
        return functools.wraps(function)(wrapped_function)

    # Allows for both `@usage.collect` and `@usage.collect(...)`.
    if function:
        return wrap(function)

    return wrap
