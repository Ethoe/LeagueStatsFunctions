# Ryan Outtrim
# 3/22/19
# Function to go through all of the champion squares to get an average hash and then save it to a hash
# Hash will be composed of an average of the values in the four corners of the square
from PIL import Image
import os
import json


class Hash:

    def creator(self):
        dictionary = dict()

        # To iterate through each file in ChampSquare folder
        for filename in os.listdir('ChampSquare'):
            currentImage = Image.open('ChampSquare/' + filename, 'r')
            avgCalc = self.averaging(currentImage)

            # Hashing the tuple to
            dictionary[','.join(map(str, avgCalc))] = filename[:-4]

        toSave = json.dumps(dictionary)
        file = open("hashes.json", "w")
        file.write(toSave)
        file.close()

    @staticmethod
    def averaging(image):
        avgCalc = [0, 0, 0]
        iterations = 0
        size = image.getbbox()

        # Assigning each champion square in the game to a tuple of the average color
        for x in range(int(size[2] / 10), size[2] - int(size[2] / 10)):
            for y in range(int(size[3] / 10), size[3] - int(size[3] / 10)):
                iterations += 1
                value = image.getpixel((x, y))
                for i in range(0, 3):
                    avgCalc[i] += value[i]

        for i in range(0, 3):
            avgCalc[i] = round(avgCalc[i] / (10 * iterations))

        return tuple(avgCalc)
