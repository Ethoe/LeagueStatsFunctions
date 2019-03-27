# Ryan Outtrim
# 3/25/19
# Generates slices of a champion splash art given hieght and width needed
from pixelValue import Imaging as im
import os
import cv2
import imutils


def slicer(maxHeight, maxWidth):
    for filename in os.listdir('ChampSquare'):
        # Extracting champion name from file
        champName = filename[:-4]
        currentSplash = cv2.imread('ChampSplash/' + champName + '.jpg')
        currentSquare = cv2.imread('ChampSquare/' + filename, 0)
        faceRegion = im.find(currentSplash, currentSquare)

        # Used to center the champions face around their height, puts them 2/3rds from the left width wise
        height = int((maxHeight - faceRegion[1]) / 2)
        width = int((maxWidth - faceRegion[2]) / 3)

        # Initializing a lot of vars
        heightDelta = maxHeight - (height * 2 + faceRegion[1])
        widthDelta = maxWidth - (width * 3 + faceRegion[2])
        bottomFix, topFix, leftFix, rightFix = 0, 0, 0, 0
        loc = faceRegion[0]

        # If it goes out of bounds in any direction, change the slice locations
        if (loc[1] - height - heightDelta) < 0:
            bottomFix = 0 - (loc[1] - height - heightDelta)
        if (loc[1] + height + faceRegion[1]) > currentSplash.shape[0]:
            topFix = (loc[1] + height + faceRegion[1]) - currentSplash.shape[0]
        if (loc[0] - width * 2) < 0:
            leftFix = 0 - (loc[0] - width * 2)
        if (loc[0] + width + faceRegion[2] + widthDelta) > currentSplash.shape[1]:
            rightFix = (loc[0] + width + faceRegion[2] + widthDelta) - currentSplash.shape[1]

        # Writing the locations with fixes included
        xTop = loc[1] - height - heightDelta + bottomFix - topFix
        xBot = loc[1] + height + faceRegion[1] + bottomFix - topFix
        yLeft = loc[0] - width * 2 + leftFix - rightFix
        yRight = loc[0] + width + faceRegion[2] + widthDelta + leftFix - rightFix

        crop = currentSplash[xTop:xBot, yLeft:yRight]

        # Saves the slice in a folder for slices under their champion name
        cv2.imwrite('ChampSlice/' + champName + ".png", crop)
        print('Cropped: ' + champName)

    return



spl = cv2.imread('ChampSelect2.png')
sqr = cv2.imread('Quit.png', 0)
find = im.find(spl, sqr, True)

print(str(find))
cv2.imshow('Match', spl)
cv2.waitKey(0)