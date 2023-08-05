from ptCrypt.Symmetric.Modes.Mode import Mode
from ptCrypt.Symmetric.BlockCipher import BlockCipher
from ptCrypt.Symmetric.Paddings.Padding import Padding
from ptCrypt.Math.base import xor


class CBC(Mode):

    def __init__(self, cipher: BlockCipher, iv: bytes, padding: Padding = None):
        super().__init__(cipher, padding)
        self.iv = iv
    
    def encrypt(self, data: bytes):
        if self.padding:
            data = self.padding.pad(data)
        
        prevBlock = self.iv
        blocks = self.splitBlocks(data)
        for i in range(len(blocks)):
            blocks[i] = self.cipher.encrypt(xor(prevBlock, blocks[i]))
            prevBlock = blocks[i]

        return self.joinBlocks(blocks)

    def decrypt(self, data: bytes):
        if len(data) % self.cipher.blockSize:
            raise BlockCipher.WrongBlockSizeException(f"Cannot process data. Data size ({len(data)}) is not multiple of the cipher block size ({self.cipher.blockSize}).")
        
        prevBlock = self.iv
        blocks = self.splitBlocks(data)
        for i in range(len(blocks)):
            t = blocks[i]
            blocks[i] = xor(self.cipher.decrypt(blocks[i]), prevBlock)
            prevBlock = t

        decrypted = self.joinBlocks(blocks)

        if self.padding:
            decrypted = self.padding.unpad(decrypted)
        
        return decrypted
