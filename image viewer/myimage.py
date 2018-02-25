"""
Class for basic manipulation with images.
Should be initiated both with filename and a temporary directory name

Functions:
.resize - resizes the image with a given ratio (float)
.rotate - rotates on 0, 90, 180, 270 degrees
.flip   - 'h': flips horizontally, 'v' flips vertically
.close  - closes the image and deletes a temporary copy
.save   - saves the image. With given filename arguments finctions as 'save as'
.delete - deletes the image file and its temporary copy

Temporary image copy names is date and time of its creation.
"""

from PIL import Image
from datetime import datetime
import os


class MyImage():

    def __init__(self, imgPath, tempPath):
        self.imgPath = imgPath
        try:
            a = Image.open(imgPath)
            self.tempName = tempPath + str(datetime.now()) \
                        + "." + a.format
            self.img = a.copy().save(self.tempName)
            a.close()
            self.img = Image.open(self.tempName)
            self.width, self.height = self.img.size
            self.format = self.img.format
        except IOError:
            raise ValueError("The file is not image file")

    def resize(self, ratio):
    #resizes with a given ratio 0.1, 5 etc
        size = (int(self.width + self.width * ratio), int(self.height + self.height * ratio))
        self.img.resize(size, Image.ANTIALIAS).save(self.tempName)
        self.img = Image.open(self.tempName)
        self.width, self.height = self.img.size


    def rotate(self, degrees):
    #rotates left/right on 90 degrees
        if degrees not in (-90, 90):
            raise ValueError("Degrees can be -90, 90")
        else:
            self.img.rotate(degrees, expand = True).save(self.tempName)
            self.img = Image.open(self.tempName)
            self.width, self.height = self.img.size


    def flip(self, direction):
    #flips 'h'orizontally or 'v'ertically
        if direction not in ("h", "v"):
            raise ValueError("Values for direction: 'h' (horizontal), 'v' (vertical)")
        else:
            if direction == "h":
                self.img.transpose(Image.FLIP_LEFT_RIGHT).save(self.tempName)
            else:
                self.img.transpose(Image.FLIP_TOP_BOTTOM).save(self.tempName)
            self.img = Image.open(self.tempName)
            self.width, self.height = self.img.size
        

    def save(self, *fileName):
    #saves the image or saves as a copy under a new name
        
        if fileName:
            try:
                self.img.save(fileName[0])
            except IOError:
                self.img.save(fileName[0] + self.format)
        else:
            self.img.save(self.imgPath)
        


    def close(self):
    #closes the image and deletes the temporary copy 
        self.img.close()
        if os.path.isfile(self.tempName):
            os.remove(self.tempName)
        else:
            print("no")

    def delete(self):
    #deletes the image
        self.close()
        os.remove(self.imgPath)

def main():
    pass

if __name__ == "__main__":
    main()
