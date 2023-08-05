from ptCrypt.Symmetric.Paddings.Padding import Padding


class PKCS5Padding(Padding):


    def __init__(self, blockSize: int) -> None:
        if blockSize > 0xff:
            raise Padding.InappropriateBlockSizeException(f"Block size is required to be in range 1..255 but {blockSize} received.")
        super().__init__(blockSize)

    def pad(self, data: bytes) -> bytes:
        count = self.blockSize - (len(data) % self.blockSize)
        return data + bytes([count]) * count
    
    def unpad(self, data: bytes) -> bytes:
        return data[:-data[-1]]