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
        self.count = 1
    
def createAverageRGBList(images):
    print "Creating average RGB list"
    averages = []
    for image in images:
        averages.append(ImageInfo(calculateAverageRGB(image)))

    return averages

def findClosestMatch(baseTileAvg, tileAvgs):
    difference = 0
    index = 0
    returnIndex = 0
    for tile in tileAvgs:
        testDifference = tile.count * (abs(baseTileAvg[0] - tile.rgbAvg[0]) + abs(baseTileAvg[1] - tile.rgbAvg[1]) + abs(baseTileAvg[2] - tile.rgbAvg[2]))
        if difference == 0 or testDifference < difference:
            difference = testDifference
            returnIndex = index
        index += 1

    tileAvgs[returnIndex].count += 1
    return returnIndex
    
def tintImageChannel(image, diff):
    image = image + diff
    np.place(image, image > 255, 255)
    np.place(image, image < 0, 0)
    return image

def tintImage(baseTileAvg, tileAvg, tileImage):
    redDiff = baseTileAvg[0] - tileAvg[0]
    greenDiff = baseTileAvg[1] - tileAvg[1]
    blueDiff = baseTileAvg[2] - tileAvg[2]
    
    returnImage = np.copy(tileImage)
    returnImage[:, :, 0] = tintImageChannel(np.int16(tileImage[:, :, 0]), blueDiff)
    returnImage[:, :, 1] = tintImageChannel(np.int16(tileImage[:, :, 1]), greenDiff)
    returnImage[:, :, 2] = tintImageChannel(np.int16(tileImage[:, :, 2]), redDiff)
    return returnImage

def generateMosaic(baseImage, tileImages, tileAvgs, mosaicSize):
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
            baseTileAvg = calculateAverageRGB(baseImage[iRow : iRow + mosaicSize, iCol : iCol + mosaicSize, :])
            matchIndex = findClosestMatch(baseTileAvg, tileAvgs)
            resultImage[iResultRow : iResultRow + tileSize, iResultCol : iResultCol + tileSize, :] = tintImage(baseTileAvg, tileAvgs[matchIndex].rgbAvg, tileImages[matchIndex])
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
    
    mosaic = generateMosaic(baseImage, images, averages, 50)
    
    print "Writing mosaic"
    cv2.imwrite("test.jpg", mosaic)