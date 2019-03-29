# Ryan Outtrim
# 3/25/19
# Function to find champ names at location of champ select
import numpy as np
import cv2
import imutils
import os

class Imaging:

    # Function to find a location of given template in full image
    @staticmethod
    def find(image, toFind, debug=False, depth=False):
        # Changes given template to a wireframe image
        toFind = cv2.Canny(toFind, 50, 200)
        found = None
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        w, h = toFind.shape[::-1]

        for smaller in range(2):
            for flipper in range(2):
                # For 20 steps in between .2 and 1 will loop different scales to find best fit
                for scale in np.linspace(.2, 1, 15)[::-1]:
                    # Resizing the full image to fit the template
                    resized = imutils.resize(grey, width=int(grey.shape[1] * scale))
                    r = grey.shape[1] / float(resized.shape[1])

                    if resized.shape[0] < h or resized.shape[1] < w:
                        break

                    # Storing values of this scale and seeing if it is higher than the current best
                    edged = cv2.Canny(resized, 50, 200)
                    result = cv2.matchTemplate(edged, toFind, cv2.TM_CCOEFF)

                    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

                    if found is None or maxVal > found[0]:
                        found = (maxVal, maxLoc, r)
                if depth:
                    break
                toFind = cv2.flip(toFind, 1)
            if depth:
                break
            toFind = toFind[15:105, 15:105]

        # Unpacking best scale and storing the info into toReturn var
        (_, maxLoc, r) = found
        start = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        end = (int((maxLoc[0] + w) * r), int((maxLoc[1] + h) * r))

        pointSize = (start, end[0] - start[0], end[1] - start[1])

        # If debug mode is on, draws a yellow rectangle around found area
        if debug:
            cv2.rectangle(image, start, end, (0, 255, 255), 2)

        return pointSize
