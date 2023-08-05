from abc import *


class Cipher(ABC):
    class UnsupportedKeyLengthException(Exception):
        pass

    @abstractproperty
    def key(self) -> bytes:
        pass

    @abstractmethod
    def __init__(self, key: bytes):
        pass
    
    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        pass