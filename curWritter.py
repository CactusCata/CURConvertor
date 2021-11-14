try:
    import numpy
except ModuleNotFoundError:
    print("module 'numpy' is not installed")
    pip.main(['install', 'numpy'])

try:
    import cv2
except ModuleNotFoundError:
    print("module 'cv2' is not installed")
    pip.main(['install', 'cv2'])

import numpy as np
import cv2 as cv
import sys
import curFileUtils
from curFileUtils import write

def generatePresenceData(size, matrix):
    presenceData = []
    bytesArraySize = size * size // 8
    if size == 48:
        bytes_7 = int(matrix[0][0][0])
        bytes_8 = int(matrix[0][0][3])
        i = 0
        while i < bytesArraySize:
            for j in range(6):
                res = (1 << 8) - 1 # = 255
                for k in range(8):
                    if matrix[(i * 8 + k) // size][(i * 8 + k) % size].tolist() != [0, 0, 0, 0]:
                        res -= 1 << (7 - k)
                i += 1
                presenceData.append(res)
            presenceData.append(bytes_7)
            presenceData.append(bytes_8)
    else:
        i = 0
        while i < bytesArraySize:
            res = (1 << 8) - 1
            for k in range(8):
                if matrix[((i * 8) + k) // size][(i * 8 + k) % size].tolist() != [0, 0, 0, 0]:
                    res -= 1 << (7 - k)
            presenceData.append(res)
            i += 1

    return presenceData

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Veuillez préciser un nom de fichier .png")
        exit()

    curFileUtils.loadFile(sys.argv[1], "rb")
    curFileUtils.unloadFile()

    if not curFileUtils.isLoaded():
        print("Echec: le fichier n'est pas chargé")
        exit()

    curFileUtils.loadFile("out.cur", "wb")

    fileInput = np.rot90(cv.flip(cv.imread(sys.argv[1], cv.IMREAD_UNCHANGED), 1), k=2)

    img128 = cv.resize(fileInput, (128, 128), interpolation = cv.INTER_CUBIC)
    img96 = cv.resize(fileInput, (96, 96), interpolation = cv.INTER_CUBIC)
    img64 = cv.resize(fileInput, (64, 64), interpolation = cv.INTER_CUBIC)
    img48 = cv.resize(fileInput, (48, 48), interpolation = cv.INTER_CUBIC)
    img32 = cv.resize(fileInput, (32, 32), interpolation = cv.INTER_CUBIC)

    imagesPNGIn = [img128, img96, img64, img48, img32]
    imagesUnknowSupSize = [2048, 1152, 512, 384, 128]
    imageSize = {32: 3200, 48: 8576, 64: 15872, 96: 36992, 128: 66560}

    cursorFile = open("out.cur", "wb")

    write(2, 0) # reserved
    write(2, 2) # type
    write(2, len(imagesPNGIn)) # image amount (count)

    imageOffset = 6 + (16 * len(imagesPNGIn))

    # ================New picture===============
    for i in range(len(imagesPNGIn)):
        imagePNG = imagesPNGIn[i]
        imageWidth = len(imagePNG)
        imageHeight = len(imagePNG[0])
        imageSizeInBytes = imageWidth * imageHeight * 4 + 40 + imagesUnknowSupSize[i]
        write(1, imageWidth) # width
        write(1, imageHeight) # height
        write(1, 0) # colorcount
        write(1, 0) # reversed
        write(2, 0) # XHotSpot
        write(2, 0) # YHotSpot
        write(4, imageSizeInBytes)
        write(4, imageOffset)
        imageOffset += imageSizeInBytes

    # =============Info Header of picture {i}==============
    for i in range(len(imagesPNGIn)):
        imagePNG = imagesPNGIn[i]
        imageWidth = len(imagePNG)
        imageHeight = len(imagePNG[0])

        # Writting header of picture
        write(4, 40) # size
        write(4, imageWidth) # width
        write(4, imageHeight * 2) # 2 * height
        write(2, 1) # planes
        write(2, 32) # bitCount
        write(4, 0) # compression
        write(4, imageSize[imageWidth]) # imageSize
        write(4, 0) # xpixelPerM
        write(4, 0) # ypixelPerM
        write(4, 0) # colorUsed
        write(4, 0) # colorImportant

        for x in range(imageWidth):
            for y in range(imageHeight):
                for d in range(4):
                    write(1, int(imagePNG[x][y][d]))
        print(f"ImageData: bytesWritted = {imageWidth * imageHeight * 4}")

        presenceData = generatePresenceData(imageWidth, imagePNG)
        for x in presenceData:
            write(1, x)
        print(f"presenceData: bytesWritted = {len(presenceData)}")

    curFileUtils.unloadFile()
