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

def chopGridFromFile(grid_x,grid_y):
    logging.info("[Start] chopGrid()")
    gridName = os.path.split(args.inputFile)[1]
    logging.info( gridName + " is " + str(grid_x) + " by " + str(grid_y))
    x_size_floor = math.floor(args.size/grid_x)
    x_size_ceil = math.ceil(args.size/grid_x)
    y_size_floor = math.floor(args.size/grid_y)
    y_size_ceil = math.ceil(args.size/grid_y)
    img =  cv2.imread(args.inputFile+"."+args.ext)
    curPiece = img[5:x_size_ceil+15,5:y_size_ceil+15]
    curPiece = img[5+24:x_size_ceil+15+24,5:y_size_ceil+15]
    print(x_size_ceil)
    print(img.shape)
    simage=Image.fromarray(curPiece)
    simage.save(os.path.join(args.outputDir,gridName,str(2)+"."+args.ext))
    logging.info("[End] chopGrid()")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the largest square in an image')
    parser.add_argument('inputFile', type=str, help="Input image file")
    parser.add_argument('grid_x', type=int, help='number of cells in x direction')  
    parser.add_argument('grid_y', type=int, help='number of cells in y direction')
    parser.add_argument('outputDir', type=str, help="Input image file")
    parser.add_argument('--ext', type=str, help="The file extension to save output images as", default='jpg')
    parser.add_argument('--size', type=int, help="The input image dim", default=500)
    parser.add_argument('--offset', type=int, help="The offset used when generating the grid. Very important that its the same", default=10)
    args = parser.parse_args()
    chopGridFromFile(args.grid_x,args.grid_y)
