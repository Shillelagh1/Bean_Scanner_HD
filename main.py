import subprocess
from bottle import run, post, request, response, get, route
import bottle
import numpy
import os
import math
import cv2  # Not actually necessary if you just want to create an image.


imageHeight = 80 #80
imageWidth = 80 #224
Xpos = 0
Ypos = 0
LoopedPosition = 0
stepDist = 0.0625
depthImage = [0]*imageWidth*imageHeight
blank_image = numpy.zeros((imageHeight*2,imageWidth,3), numpy.uint8)
response = bottle.BaseResponse()


def calculatePosition(position, depth, size):
    return (position - (depth / 2)) * size

def deLoop(loopedPosition, width):
    x = loopedPosition % width
    print(x)
    y = numpy.floor(loopedPosition/width)
    print(y)
    return [x,y]

@route("/try/<number>")
def tryHTTP(number):
    print("Try")
    print(number)
    response.body = number
    return response

@route("/try/<x>,<y>")
def tryHTTP(x,y):
    print("Try")
    print(str(x)+ ", " + str(y))
    response.body = 1
    return response

@route("/begin")
def beginHTTP():
    print("Begin")
    global LoopedPosition
    LoopedPosition = 0
    global depthImage
    depthImage = [0]*imageWidth*imageHeight
    X = calculatePosition(Xpos, imageWidth, stepDist)
    Y = calculatePosition(Ypos, imageHeight, stepDist)
    response = "x={0};y={1}".format(X,Y)
    print(response)
    return response

@route("/store_NextStep/<d>")
def nextStepStore(d):
    global  depthImage
    global LoopedPosition
    global blank_image
    d = float(d)
    #Write the pixel to the image please!
    position = deLoop(LoopedPosition, imageWidth)
    blank_image[int(position[1]),int(position[0])] = [math.floor(d*100),0,0]
    #Write the next pixel to scan to the camera buffer (math)
    LoopedPosition = LoopedPosition + 1
    position = deLoop(LoopedPosition,imageWidth)
    #Buffer store
    X = calculatePosition(position[0], imageWidth, stepDist)
    Y = calculatePosition(position[1], imageHeight, stepDist)
    return "x={0};y={1}".format(X,Y)

@route("/writeOut")
def writeOut():
    cv2.imwrite("image.jpg", blank_image)

@route("/frameBL")
def frameBL():
    print("frame")
    X = calculatePosition(0, imageWidth, stepDist)
    Y = calculatePosition(0, imageHeight, stepDist)
    response = "x={0};y={1}".format(X,Y)
    return response

@route("/frameUL")
def frameUL():
    print("frame")
    X = calculatePosition(0, imageWidth, stepDist)
    Y = calculatePosition(imageHeight, imageHeight, stepDist)
    response = "x={0};y={1}".format(X,Y)
    return response

@route("/frameUR")
def frameUL():
    print("frame")
    X = calculatePosition(imageWidth, imageWidth, stepDist)
    Y = calculatePosition(imageHeight, imageHeight, stepDist)
    response = "x={0};y={1}".format(X,Y)
    return response


@route("/frameBR")
def frameBR():
    print("frame")
    X = calculatePosition(imageWidth, imageWidth, stepDist)
    Y = calculatePosition(0, imageHeight, stepDist)
    response = "x={0};y={1}".format(X,Y)
    return response

print("Starting")
run(host='localhost', port=8080, debug=True)

