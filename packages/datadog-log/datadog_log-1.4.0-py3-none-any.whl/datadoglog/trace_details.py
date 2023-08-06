import os
import warnings

from typing import Callable, Mapping


def get_trace_details_provider() -> Callable[[], Mapping]:
    def noop():
        return {}

    if os.getenv("DD_LOGS_INJECTION") != "true":
        return noop
    try:
        from ddtrace import tracer
    except ImportError:
        warnings.warn("DD_LOGS_INJECTION is set but ddtrace is not installed")
        return noop

    def details():
        span = tracer.current_span()
        if not span:
            return {}
        return {
            "dd.trace_id": span.trace_id,
            "dd.span_id": span.span_id,
        }

    return details
