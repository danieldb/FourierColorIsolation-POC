import imp
import math
import heapq


'''
this class takes a processed image and it's derivative and finds the points that an object is over

1. loop through the derivative looking for points in which 
    d/dx = 0 but f(x) is high (this means that you look for a 
    point at which there is a bright color and is in the middle of
    a pseudo-elliptical gradient created by the blurred color)
2. append each of those coordinates and values to a list
3. loop through those maxes and choose the largest ones
4. create an image to display what we have found
'''
class ImMaxer:
    def __init__(self):
        pass

    def maxValues(self, derivative, demag_spec, number, threshold):
        allMaxes = []
        maxCoords = []
        for i in range(len(derivative)):
            for e in range(len(derivative[i])):
                if derivative[i][e] >= 0 and derivative[i][e] <= 1: # possibly switch to within a threshold of zero if it works better that way
                    if demag_spec[i][e] >= threshold:
                        maxCoords.append([e, i])
                        allMaxes.append(abs(math.floor(demag_spec[i][e])))
                        print('mc: ', demag_spec[i][e])
        selectedMaxes = []
        for i in range(number):
            #selectedMaxes.append(heapq.nlargest(number, range(len(allMaxes)), key=allMaxes.__getitem__))
            if(len(heapq.nlargest(number, range(len(allMaxes)), key=allMaxes.__getitem__)) > i):
                idx = heapq.nlargest(number, range(len(allMaxes)), key=allMaxes.__getitem__)[i]
                selectedMaxes.append(maxCoords[idx])
                print('sel!')
        print(allMaxes)
        print(selectedMaxes)
        return selectedMaxes


    def createMaxesImage(self, newImg, selectedMaxes):
        emt=[]
        for i in range(len(newImg)):
            newList = []
            for e in range(len(newImg[0])):
                newList.append(0)
            emt.append(newList)

        for i in selectedMaxes:
            emt[i[1]][i[0]] = 255
        return emt
        