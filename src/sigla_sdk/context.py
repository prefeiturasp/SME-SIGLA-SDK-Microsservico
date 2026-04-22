import threading
from typing import Optional

_thread_locals = threading.local()


def get_correlation_id() -> Optional[str]:
    return getattr(_thread_locals, "correlation_id", None)


def set_correlation_id(value: Optional[str]) -> None:
    _thread_locals.correlation_id = value


def get_auth_header() -> Optional[str]:
    return getattr(_thread_locals, "auth_header", None)


def set_auth_header(value: Optional[str]) -> None:
    _thread_locals.auth_header = value


def clear_request_context() -> None:
    _thread_locals.correlation_id = None
    _thread_locals.auth_header = None

