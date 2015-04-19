import cv2
import numpy as np
import sys
import os

def readTileImages():
    print "Reading tile images"
    tileFolder = os.path.abspath(os.path.join(os.curdir, 'tilePhotos'))

    # Extensions recognized by opencv
    exts = ['.jpeg', '.jpg', '.jpe', '.png']
    img_list = []
    filenames = sorted(os.listdir(tileFolder))

    for filename in filenames:
        name, ext = os.path.splitext(filename)
        if ext.lower() in exts:
            img_list.append(cv2.imread(os.path.join(tileFolder, filename)))

    return img_list
    
def readBaseImage():
    print "Reading base image"
    baseFolder = os.path.abspath(os.path.join(os.curdir, 'basePhoto'))

    # Extensions recognized by opencv
    exts = ['.jpeg', '.jpg', '.jpe', '.png']
    filenames = sorted(os.listdir(baseFolder))
    if len(filenames) != 1:
        print "Error reading base image"
        sys.exit()

    image = []
    for filename in filenames:
        name, ext = os.path.splitext(filename)
        if ext.lower() in exts:
            image = cv2.imread(os.path.join(baseFolder, filename))

    return image

def calculateAverageRGB(image):
    imagePixels = image.shape[0] * image.shape[1]
    blueAvg = np.sum(image[:, :, 0])/imagePixels
    greenAvg = np.sum(image[:, :, 1])/imagePixels
    redAvg = np.sum(image[:, :, 2])/imagePixels
    
    return redAvg, greenAvg, blueAvg

class ImageInfo:
    def __init__(self, avg):
        self.rgbAvg = avg
        self.count = 0
    
def createAverageRGBList(images):
    print "Creating average RGB list"
    averages = []
    for image in images:
        averages.append(ImageInfo(calculateAverageRGB(image)))

    return averages

def findClosestMatch(tileAvg, tileImages):
    return tileImages[0]
    
def generateMosaic(baseImage, tileImages, mosaicSize):
    print "Creating mosaic"
    
    tileSize = tileImages[0].shape[0]
    iRows = baseImage.shape[0]
    iCols = baseImage.shape[1]
    
    resultImage = np.zeros(((baseImage.shape[0] / mosaicSize) * tileSize, (baseImage.shape[1] / mosaicSize) * tileSize, 3), np.uint8)
    iResultRow = 0
    iRow = 0
    while iRow < iRows:
        iCol = 0
        iResultCol = 0
        while iCol < iCols:
            if iResultCol == 1000:
                k = 12
            tileAvg = calculateAverageRGB(baseImage[iRow : iRow + mosaicSize, iCol : iCol + mosaicSize, :])
            #print "iResultRow: " + str(iResultRow) + " - iResultCol: " + str(iResultCol) + " - iRow: " + str(iRow) + " - iCol: " + str(iCol)
            resultImage[iResultRow : iResultRow + tileSize, iResultCol : iResultCol + tileSize, :] = findClosestMatch(tileAvg, tileImages)
            iCol += mosaicSize
            iResultCol += tileSize
        
        iRow += mosaicSize
        iResultRow += tileSize
        
    return resultImage

if __name__ == "__main__":
    print "Begin mosaic generation"
    
    images = readTileImages()
    if len(images) <= 0:
        print "Error reading tile images"
        sys.exit()
    
    averages = createAverageRGBList(images)
    
    print str(len(images))
    baseImage = readBaseImage()
    
    mosaic = generateMosaic(baseImage, images, 50)
    cv2.imwrite("test.jpg", mosaic)