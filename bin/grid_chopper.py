#! /usr/bin/env python3
#
# Author: David Vasko

import cv2
from PIL import Image
import numpy as np
import logging
import argparse
import os
import math

logging.basicConfig(filename='crossy.log',level=logging.INFO)
global args

def saveImage(img,fullName):
    simage=Image.fromarray(img)
    simage.save(fullName)

def chopGridAtPoint(img,pt,x_size,y_size,offset):
    dx = (offset+x_size)/2
    dy = (offset+y_size)/2
    crop = img[pt[0]-dx:pt[0]+dx,pt[1]-dy:pt[1]+dy]
    return crop
    
def chopColumn(img,pt,x_size,y_size,offset,grid_x,gridName):
    
    logging.debug("Processing column: ["+str(pt[1])+"]")
    colPts = [[pt[0]+x_size*i,pt[1]] for i in range(grid_x)]
    
    # loop throuhg points 
    for pt in colPts:
        crop = chopGridAtPoint(img,pt,x_size,y_size,args.offset)
        if not os.path.exists(os.path.join(args.outDir,gridName)):
            os.makedirs(os.path.join(args.outDir,gridName))
        saveImage(crop,os.path.join(args.outDir,gridName,str(pt[0])+"-"+str(pt[1])+"."+args.ext))
    

def chopGridFromFile(grid_x,grid_y):
    logging.info("[Start] chopGrid()")
    
    # Open file and log
    gridName = os.path.split(args.inputFile)[1]
    logging.info( gridName + " is " + str(grid_x) + " by " + str(grid_y))
    
    # First need to find various dimensions of the grid
    x_size = (args.size_x-args.offset)/grid_x
    y_size = (args.size_y-args.offset)/grid_y
    
    # Lod the image
    img =  cv2.imread(args.inputFile+"."+args.ext)
    
    # seed positions
    pts = [[args.offset+x_size/2,args.offset+y_size/2+y_size*i] for i in range(grid_y)] 
    coordinates = [[0,i] for i in range(grid_y)]
    
    # chop each column (can do in own thread later)
    for pt in pts:
        chopColumn(img,pt,x_size,y_size,args.offset,grid_x,gridName)
    # i should draw squares on original image so i can see visually have to account for rounding...
    logging.info("[End] chopGrid()")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the largest square in an image')
    parser.add_argument('inputFile', type=str, help="Input image file")
    parser.add_argument('grid_x', type=int, help='number of cells in x direction')  
    parser.add_argument('grid_y', type=int, help='number of cells in y direction')
    parser.add_argument('outDir', type=str, help="Input image file")
    parser.add_argument('--ext', type=str, help="The file extension to save output images as", default='jpg')
    parser.add_argument('--size_x', type=int, help="The input image dim", default=500)
    parser.add_argument('--size_y', type=int, help="The input image dim", default=500)
    parser.add_argument('--offset', type=int, help="The offset used when generating the grid. Very important that its the same", default=10)
    args = parser.parse_args()
    chopGridFromFile(args.grid_x,args.grid_y)
