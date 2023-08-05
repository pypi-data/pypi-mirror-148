"""FastAPI MVC Command abstract class implementation.

The fastapi-mvc.commands submodule implements command design pattern:
https://refactoring.guru/design-patterns/command
"""
from abc import ABCMeta, abstractmethod
import logging


class Command(object, metaclass=ABCMeta):
    """Defines the common interface for all concrete commands.

    Attributes:
        _log (logging.Logger): Logger class object instance.

    """

    __slots__ = "_log"

    def __init__(self):
        """Initialize Command base class object instance."""
        self._log = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def execute(self):
        """Abstract method execute for all inheriting classes."""
        pass
