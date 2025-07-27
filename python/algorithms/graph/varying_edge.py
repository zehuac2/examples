from abc import ABC, abstractmethod


class VaryingEdge(ABC):
    """Interface for edges with varying lengths."""

    @property
    @abstractmethod
    def length(self) -> int:
        """Length of the edge."""
        pass
