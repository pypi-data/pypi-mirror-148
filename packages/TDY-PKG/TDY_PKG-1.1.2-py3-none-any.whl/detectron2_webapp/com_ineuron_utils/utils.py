import base64
# import os
# import sys
# from pathlib import Path
# FILE = Path(__file__).resolve()
# ROOT = str(FILE.parents[1])
# sys.path.insert(0, ROOT)

def decodeImagedetectron(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    # with open(ROOT+"/"+fileName, 'wb') as f:
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())