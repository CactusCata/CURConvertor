from feeder import Feeder

class Cur(Feeder):

    def __init__(self):
        super().__init__()
        self.imagesCur = []

    def appendImageCur(self, imageCur):
        self.imagesCur.append(imageCur)

    def getImageCur(self, index):
        return self.imagesCur[index]

    def __str__(self):
        toSend = super().__str__()
        for imageCur in self.imagesCur:
            toSend += str(imageCur)
        return toSend
