from enum import StrEnum

class Bitrate(StrEnum):
    """
    Enum para los bitrates

    Attributes:
        B_48K (str): 48Kbps
        B_56K (str): 56Kbps
        B_64K (str): 64Kbps
        B_96K (str): 96Kbps
        B_128K (str): 128Kbps
        B_192K (str): 192Kbps
        B_256K (str): 256Kbps
        B_320K (str): 320Kbps
    """
    B_48K = "48k"
    B_56K = "56k"
    B_64K = "64k"
    B_96K = "96k"
    B_128K = "128k"
    B_192K = "192k"
    B_256K = "256k"
    B_320K = "320k"

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value