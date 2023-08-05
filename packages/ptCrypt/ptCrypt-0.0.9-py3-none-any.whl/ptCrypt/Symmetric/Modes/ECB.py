from ptCrypt.Symmetric.Modes.Mode import Mode
from ptCrypt.Symmetric.BlockCipher import BlockCipher
from ptCrypt.Symmetric.Paddings.Padding import Padding

class ECB(Mode):
    """Electronic codebook mode of encryption. The simplest encryption mode. 
    Encrypts every block independently from other blocks.

    More: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB)
    """

    def __init__(self, cipher: BlockCipher, padding: Padding = None):
        super().__init__(cipher, padding)
    
    def encrypt(self, data: bytes):
        if self.padding:
            data = self.padding.pad(data)
        
        blocks = self.splitBlocks(data)
        for i in range(len(blocks)):
            blocks[i] = self.cipher.encrypt(blocks[i])

        return self.joinBlocks(blocks)
    
    def decrypt(self, data: bytes):
        if len(data) % self.cipher.blockSize:
            raise BlockCipher.WrongBlockSizeException(f"Cannot process data. Data size ({len(data)}) is not multiple of the cipher block size ({self.cipher.blockSize}).")

        blocks = self.splitBlocks(data)
        for i in range(len(blocks)):
            blocks[i] = self.cipher.decrypt(blocks[i])
        decrypted = self.joinBlocks(blocks)

        if self.padding:
            decrypted = self.padding.unpad(decrypted)
        
        return decrypted
