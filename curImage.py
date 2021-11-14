from feeder import Feeder

class CurImage(Feeder):
    """
    Each image contains these informations
    """

    def __init__(self):
        super().__init__()
        self.infoHeader = Feeder()

    def setPresenceBytesLength(self, presenceBytesLength):
        self.presenceBytesLength = presenceBytesLength

    def getPresenceBytesLength(self):
        return self.presenceBytesLength

    def getInfoHeader(self):
        return self.infoHeader

    def setImageData(self, imageData):
        """
        image data is a matrix in 3 dimensions:
        imageData[width][height][r, g, b, a]
        """
        self.imageData = imageData

    def getImageData(self):
        return self.imageData

    def setPresenceData(self, presenceData):
        """
        presenceData is an array of byte
        """
        self.presenceData = presenceData

    def getPresenceData(self):
        return self.presenceData
