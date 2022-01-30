import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from ImMaxer import ImMaxer
from ImPrep import ImPrep
from ImProc import ImProc

'''
this program takes an image and finds where objects of a certain color are in frame

it uses fft applied to images and filters on their transforms

this program I consider relatively fast for python, especially considering the 
alternative being checking each pixel then applying kernel based processing

NOTE: make sure all your libraries are installed before running, this includes the 
      ones that are in 'ImMaxer.py' 'ImPrep.py' and 'ImProc.py'
'''

# for later when rendering images
fig = plt.figure()
def loadim(arr, title, x, y, num):
    ax = fig.add_subplot(y,x,num)
    ax.imshow(arr, cmap='gray')
    plt.title(title)
    plt.xticks([])
    plt.yticks([])

# prepare image
prep = ImPrep()

img = prep.loadpic("elements.jpg")

resized = prep.resizePic(img, 128/len(img[0]) * 100 )

newIm = prep.processForColorBGR(resized)

print('forier')

# do the fft shit
proc = ImProc()

fshift = proc.forier(newIm)

premag_spec = proc.format_for_display(fshift)

# processing (low pass for blur) 
lshift = proc.lowpass(fshift=fshift, scale=10)
magnitude_spectrum = proc.format_for_display(lshift)

# defft
fs = proc.deforier(lshift)
demag_spec = np.abs(fs) # this returns negative values, so abs


# calculte the derivative of the image (https://docs.opencv.org/3.4/d2/d2c/tutorial_sobel_derivatives.html)
derivative = proc.imgDerivative(demag_spec)

# get those maxes
maxer = ImMaxer()

selectedMaxes = maxer.maxValues(derivative, demag_spec, 4, 20) # optimal threshold and number depends on image conditions (haha 420)
selectedMaxes = maxer.noDupes(selectedMaxes, 1) # distance depends on other factors

emt=maxer.createMaxesImage(newIm, selectedMaxes)


#draw images

#input image
loadim(newIm, "Original Image", 3, 2, 1)
#fourier transform of input image
loadim(premag_spec, "Forier Transformed Image", 3, 2, 2)
#filter of fourier transform image
loadim(magnitude_spectrum, "Filtered Forier Transform", 3, 2, 3)
#reverted image from fourier transform filter (blurred)
loadim(demag_spec, "Reverted Image", 3, 2, 4)
#derivative of blurred image
loadim(derivative, "derivative", 3, 2, 6)
#target points image
loadim(emt, "targets", 3, 2, 5)

plt.show()