#! /usr/bin/env python3
#
# Author: David Vasko

import cv2
from PIL import Image
import numpy as np
import logging
import argparse

logging.basicConfig(filename='crossy.log',level=logging.INFO)
global args

def outputVertices(verts,imgDim,offset=10):
    max = np.amax(verts)
    min = np.amin(verts)
    ret = np.round(np.divide(np.subtract(verts,min),max-min)).astype(int)
    ret[ret==0] = offset
    ret[ret==1] = imgDim-offset
    logging.debug(ret)
    return ret
    
    
def findGrid():
    logging.debug("[Start] findGrid()")
    imgDim=args.size
    inputFile=args.inputFile+"."+args.ext
    outFile=args.inputFile+"_cropped."+args.ext
    outFileBox=args.inputFile+"_boxed."+args.ext
    outFileThresh=args.inputFile+"_thresh."+args.ext
    outFileContours=args.inputFile+"_contours."+args.ext

    img =  cv2.imread(inputFile)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.fastNlMeansDenoising(gray,gray,7,21,5) 

    gray = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
    simage=Image.fromarray(thresh)
    simage.save(outFileThresh)

    img2, contours, heirachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    biggest = None
    max_area = 0
    for i in contours:
            area = cv2.contourArea(i)
            if area > 100:
                peri = cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,0.02*peri,True)
                area1 = cv2.contourArea(approx);
                
                if area > max_area and len(approx)==4:
                        biggest = approx
                        max_area = area  
                        
    logging.debug("Max Area is:" + str(max_area))
    logging.debug("Vertices of max are:" + str(biggest))
    cv2.drawContours(img,[biggest],-1,(0,255,0), 3)
    simage=Image.fromarray(img)
    simage.save(outFileBox)
    cv2.drawContours(img,contours,-1,(0,255,0), 3)
    simage=Image.fromarray(img)
    simage.save(outFileContours)

    pts1 = np.float32(biggest)
    pts2 = np.float32(outputVertices(biggest,imgDim))
    print(pts1)
    print(pts2)
    M = cv2.getPerspectiveTransform(pts1,pts2)
    thumbnail = cv2.warpPerspective(gray, M, (imgDim, imgDim))
    simage=Image.fromarray(thumbnail)
    simage.save(outFile)
    logging.debug("[End] findGrid()")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the largest square in an image')
    parser.add_argument('inputFile', type=str, help="Input image file")  
    parser.add_argument('--ext', type=str, help="The file extension to save images as", default='jpg')
    parser.add_argument('--size', type=int, help="The out put image dim", default=500)
    args = parser.parse_args()
    findGrid()
