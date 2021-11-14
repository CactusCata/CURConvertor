import os
import struct

BYTES_FORMAT = {1: 'B', 2:'H', 4:'I'}

curFile = None

def loadFile(path, mode):
    global curFile

    if not os.path.isfile(path) and (mode == "r" or mode == "rb"):
        print(f"The file {path} don't exist !")
        return

    curFile = open(path, mode)
    print(f"curFile \"{path}\" in mode {mode} is loaded.")


def unloadFile():
    if isLoaded():
        curFile.close()
        print(f"curFile is unloaded.")
    else:
        print(f"Can't unload a non-loaded file")

def isLoaded():
    return curFile != None

def read(bytesAmountToRead):
    return struct.unpack(BYTES_FORMAT[bytesAmountToRead], curFile.read(bytesAmountToRead))[0]

def write(byteAmount, value):
    if type(value) != int:
        raise Exception(f"The second argument need to be an int (not a {type(value)})")
    curFile.write(struct.pack(BYTES_FORMAT[byteAmount], value))
