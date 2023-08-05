from ptCrypt.Math.base import pad
from ptCrypt.Symmetric.Paddings.Padding import Padding


class ZeroPadding(Padding):

    def __init__(self, blockSize: int) -> None:
        super().__init__(blockSize)
    
    def pad(self, data: bytes) -> bytes:
        return pad(data, self.blockSize)
    
    def unpad(self, data: bytes) -> bytes:
        return data.rstrip(b"\x00")