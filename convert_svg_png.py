
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF , renderPM
import cv2
import numpy as np

svg = svg2rlg("matches/GeometricAdjacencyMatrix-src.svg")
renderPM.drawToFile(svg , "GeometricAdjacencyMatrix-src.png" , fmt='PNG')

svg_libvot = svg2rlg("matches/GeometricAdjacencyMatrix.svg")
renderPM.drawToFile(svg_libvot , "GeometricAdjacencyMatrix-libvot.png" , fmt='PNG')
def computeIOU(img , img_libvot):
    _ , binary = cv2.threshold(img , 128 , 255 , cv2.THRESH_BINARY_INV)
    _ , binary_libvot = cv2.threshold(img_libvot , 128 , 255 , cv2.THRESH_BINARY_INV)

    binary = binary/255
    binary_libvot = binary_libvot/255
    intersection = np.sum(binary * binary_libvot)
    print('intersection: ' , intersection)
    binary = binary == 1
    binary_libvot = binary_libvot == 1
    union = np.sum(binary + binary_libvot)
    print('union: ' , union)
    return intersection/union


if __name__ == '__main__':
    img = cv2.imread("GeometricAdjacencyMatrix-src.png" , 0)
    img_libvot = cv2.imread("GeometricAdjacencyMatrix-libvot.png" , 0)

    iou = computeIOU(img , img_libvot)
    print('iou: ' , iou)








