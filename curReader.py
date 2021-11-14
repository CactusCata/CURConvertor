from curImage import CurImage
from cur import Cur
import sys
import curFileUtils
from curFileUtils import read

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Veuillez préciser un nom de fichier .cur")
        exit()

    curFileUtils.loadFile(sys.argv[1], "rb")

    if not curFileUtils.isLoaded():
        print("Echec: le fichier n'est pas chargé")
        exit()

    cur = Cur()

    cur.set("reserved", read(2)) # Toujours égal à 0
    cur.set("type", read(2)) # Toujours égal à 2
    cur.set("count", read(2)) # Varie en fonction du nombre d'image total
    count = cur.get("count")

    for i in range(count):
        print("================New picture===============")
        curImage = CurImage()
        curImage.set("width", read(1))
        curImage.set("height", read(1))
        curImage.set("colorCount", read(1)) # Toujours égal à 0
        curImage.set("reversed", read(1)) # Toujours égal à 0
        curImage.set("XHotSpot", read(2)) # Toujours à 0 chez moi
        curImage.set("YHotSpot", read(2)) # Toujours à 0 chez moi
        curImage.set("sizeInBytes", read(4))
        curImage.set("fileOffset", read(4)) # Valeur égal où commence InfoHeader pour le 1er puis ensuite fileOffset_(n+1) = fileOffset_n - sizeInBytes

        sizeInBytes = curImage.get("sizeInBytes")
        width = curImage.get("width")
        height = curImage.get("height")
        curImage.setPresenceBytesLength(sizeInBytes - (width * height * 4 + 40))

        cur.appendImageCur(curImage)

    for i in range(count):
        curImage = cur.getImageCur(i)

        print(f"=============Info Header of picture {i}==============")
        infoHeader = curImage.getInfoHeader()
        infoHeader.set("size", read(4)) # toujours à 40
        infoHeader.set("width", read(4)) # width
        infoHeader.set("height", read(4)) # 2 * height
        infoHeader.set("planes", read(2)) # Toujours à 1
        infoHeader.set("bitCount", read(2)) # A 32 chez moi
        infoHeader.set("compression", read(4)) # Toujours à 0
        infoHeader.set("imageSize", read(4)) # imageWidth * imageHeight * 4 + partie presence
        infoHeader.set("xpixelPerM", read(4)) # Toujours à 0
        infoHeader.set("ypixelPerM", read(4)) # Toujours à 0
        infoHeader.set("colorUsed", read(4)) # Toujours à 0
        infoHeader.set("colorImportant", read(4)) # Toujours à 0

        print(f"==============Reading picture {i}...=================")

        imageData = []
        for j in range(curImage.get("width") * curImage.get("height")):
            imageData.append([read(1), read(1), read(1), read(1)])
        curImage.setImageData(imageData)

        print(f"============Reading unknow part of picture {i}===============")

        presenceData = []
        for j in range(curImage.getPresenceBytesLength()):
            presenceData.append(read(1))
        curImage.setPresenceData(presenceData)

    curFileUtils.unloadFile()
