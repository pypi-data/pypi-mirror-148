from abc import *


class Padding(ABC):

    class InappropriateBlockSizeException(Exception):
        pass

    @property
    def blockSize(self) -> int:
        return self._blockSize

    @abstractmethod
    def __init__(self, blockSize: int):
        self._blockSize = blockSize
    
    @abstractmethod
    def pad(self, data: bytes) -> bytes:
        pass
    
    @abstractmethod
    def unpad(self, data: bytes) -> bytes:
        pass