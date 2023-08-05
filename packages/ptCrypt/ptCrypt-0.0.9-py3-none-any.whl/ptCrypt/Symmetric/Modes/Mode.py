from abc import *
from ptCrypt.Symmetric.Cipher import Cipher
from ptCrypt.Symmetric.BlockCipher import BlockCipher
from ptCrypt.Symmetric.Paddings.Padding import Padding


class Mode(Cipher):

    class UnpaddedDataException(Exception):
        pass

    @property
    def key(self) -> bytes:
        return self.cipher.key

    @property
    def padding(self) -> Padding:
        return self._padding
    
    def __init__(self, cipher: BlockCipher, padding: Padding = None):
        super().__init__(cipher.key)
        self._padding = padding
        self.cipher = cipher
    
    def splitBlocks(self, data: bytes) -> list:
        if len(data) % self.cipher.blockSize:
            message = f"Data size ({len(data)}) is not multiple of cipher block size {self.cipher.blockSize}. Ensure that you are using correct padding or pass the data of the appropriate length."
            raise Mode.UnpaddedDataException(message)
        
        return [
            data[i * self.cipher.blockSize: i * self.cipher.blockSize + self.cipher.blockSize] 
                for i in range(len(data) // self.cipher.blockSize)
        ]
    
    def joinBlocks(self, blocks: list) -> bytes:
        return b"".join(blocks)