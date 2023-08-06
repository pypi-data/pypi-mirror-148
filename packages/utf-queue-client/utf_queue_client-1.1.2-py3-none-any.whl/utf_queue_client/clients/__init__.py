import logging
from contextlib import contextmanager
from typing import Union, List
from logging import DEBUG, INFO, WARNING, CRITICAL
from opentelemetry import trace
from functools import wraps
import inspect


__all__ = ["configure_logger", "get_logger", "Loggable", "classproperty"]

def create_span_decorator():

    def span_decorator(f):
        @wraps(f)
        def new_f(*args, **kwargs):
            module_name = __name__
            module = inspect.getmodule(f)
            if module is not None:
                module_name = module.__name__
            with trace.get_tracer(module_name).start_as_current_span(f.__qualname__, kind=trace.SpanKind.CLIENT):
                return f(*args, **kwargs)

        return new_f

    return span_decorator

class classproperty(property):
    """Helper class for defining a class method as a property"""

    def __get__(self, cls, owner):  # noqa
        return classmethod(self.fget).__get__(None, owner)()


class Loggable:
    LOG_DEBUG = DEBUG
    LOG_INFO = INFO
    LOG_WARNING = WARNING
    LOG_CRITICAL = CRITICAL

    @classproperty
    def logger(cls) -> logging.Logger:  # noqa
        """Returns a logger specific to the derived class' name"""
        return get_logger(cls.__name__)

    @contextmanager
    def set_log_level(self, level: Union[int, str]):
        old_level = self.logger.level
        try:
            self.logger.setLevel(level)
            yield
        finally:
            self.logger.setLevel(old_level)


def configure_logger():
    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m-%d-%Y %H:%M:%S",
        level=logging.INFO,
    )


def get_logger(name: str = None) -> logging.Logger:
    configure_logger()
    return logging.getLogger(name)
