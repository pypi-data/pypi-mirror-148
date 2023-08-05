from abc import ABCMeta, abstractmethod


class Interface(object, metaclass=ABCMeta):
    """Base class for all interfaces in pyobs."""

    __module__ = "pyobs.interfaces"
    pass


__all__ = ["Interface"]
