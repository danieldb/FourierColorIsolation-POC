import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv


'''
this class does all the hard work with processing the image

1. fourier transforms the input image
2. formats that transform for viewing
3. low pass filters the fourier transform (it gets rid of the fine details of the input leaving only blurry edges)
4. formats that low pass for viewing
5. takes the low pass and turns it back into a blurry form of the input
6. formats that de-fourier transformed image for viewing
5. takes the formatted low pass and calculates its discrete derivative (just imagive a derivative, but of an image)
6. formats the derivative for viewing

NOTE: there are some unused functions like bandpass, inv-bandpass, and highpass that are not used.
'''
class ImProc:
    def __init__(self):
        self.on = True

    def forier(self, arr):
        f = np.fft.fft2(arr)
        # transform the fft for better viewing
        fshift = np.fft.fftshift(f) 
        return fshift

    def deforier(self, fshift):
        fushift = np.fft.ifftshift(fshift)
        fs = np.fft.ifft2(fushift)
        return fs
    #blur
    def lowpass(self, fshift, scale=10):
        i, e = 0, 0
        for i in range(len(fshift)):
            for e in range(len(fshift[i])):
                print(i, e, fshift[i][e])
                if pow(e-len(fshift[i])/2,2)+pow(i-len(fshift)/2,2)>scale:
                    fshift[i][e] = 0.001
        return fshift

    #derivative
    def bandpass(self, fshift, min=10, max=30):
        i, e = 0, 0
        for i in range(len(fshift)):
            for e in range(len(fshift[i])):
                print(i, e, fshift[i][e])
                if pow(e-len(fshift[i])/2,2)+pow(i-len(fshift)/2,2)>min and pow(e-len(fshift[i])/2,2)+pow(i-len(fshift)/2,2)<max:
                    fshift[i][e] = 0.001
        return fshift

    #inverted derivative?
    def invbandpass(self, fshift, min=10, max=30):
        i, e = 0, 0
        for i in range(len(fshift)):
            for e in range(len(fshift[i])):
                print(i, e, fshift[i][e])
                if pow(e-len(fshift[i])/2,2)+pow(i-len(fshift)/2,2)<min or pow(e-len(fshift[i])/2,2)+pow(i-len(fshift)/2,2)>max:
                    fshift[i][e] = 0.001
        return fshift

    #edge
    def highpass(self, fshift, scale=10):
        i, e = 0, 0
        for i in range(len(fshift)):
            for e in range(len(fshift[i])):
                print(i, e, fshift[i][e])
                if pow(e-len(fshift[i])/2,2)+pow(i-len(fshift)/2,2)<scale:
                    fshift[i][e] = 0.001
        return fshift

    def format_for_display(self, fshift):
        return 20*np.log(np.abs(fshift))

    def imgDerivative(self, demag_spec):
        scale = 1
        delta = 0
        ddepth = cv.CV_16S
        grad_x = cv.Sobel(demag_spec, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
        grad_y = cv.Sobel(demag_spec, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)

        abs_grad_x = cv.convertScaleAbs(grad_x)
        abs_grad_y = cv.convertScaleAbs(grad_y)
        derivative = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        return derivative