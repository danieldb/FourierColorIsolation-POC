import math
from time import sleep
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

from ImProc import ImProc


'''
this class prepares images to be processed by 'ImProc'

1. load the picture
2. resize the picture, downscaling it to ten percent
3. convert the picture's normal opencv color (BGR) to HLS
4. process the image targeting a specific HLS band of color
5. that hls band of color is saved to a new greyscale image which 
    has that color significantly highlighted and the rest dimmed (the 
    rest is dimmed as not to mess up the fourier transform)
'''
class ImPrep:
    def __init__(self):
        pass
        

    def loadpic(self, filename):
        return cv.imread('./pics/' + filename, cv.IMREAD_UNCHANGED)

    
    def resizePic(self, img, percent):
        width = int(img.shape[1] * percent / 100)
        height = int(img.shape[0] * percent / 100)
        dim = (width, height)
        # resize image
        return cv.resize(img, dim, interpolation = cv.INTER_AREA)

    def recolorHLS(self, img):
        return cv.cvtColor(img, cv.COLOR_BGR2HLS)

    def recolorGRAY(self, img):
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    def processForColorBGR(self, img, hmax=44, hmin=19, lmax=0.892, lmin=0.525, smax=1, smin=0.736):
        img = self.recolorHLS(img)
        newIm = self.recolorGRAY(img)
        for i in range(len(img)):
            for e in range(len(img[i])):
                j = img[i][e]
                print(j)
                if (
                    j[0] < hmax and j[0] > hmin and 
                    j[1]/255 < lmax and j[1]/255 > lmin and 
                    j[2]/255 < smax and j[2]/255 > smin ):
                    newIm[i][e] = 200
                else:
                    newIm[i][e] /= 1000 # setting to 0 messes up the forier transform

        return newIm
    