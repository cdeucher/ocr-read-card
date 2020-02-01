# USAGE
from pyzbar import pyzbar
import cv2, os, sys

image = cv2.imread("../cut/bar2.jpg")

#https://stackoverflow.com/questions/50080949/qr-code-detection-from-pyzbar-with-camera-image
'''
  flip image color black-in-white
'''
mask = cv2.inRange(image,(0,0,0),(200,200,200))
thresholded = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
inverted = 255-thresholded # black-in-white
'''
  
'''

barcodes = pyzbar.decode(inverted)

barcodeData = ''
print('barcodes',barcodes)

# loop over the detected barcodes
for barcode in barcodes:
    # extract the bounding box location of the barcode and draw the
    # bounding box surrounding the barcode on the image
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # the barcode data is a bytes object so if we want to draw it on
    # our output image we need to convert it to a string first
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type

    # draw the barcode data and barcode type on the image
    text = "{} ({})".format(barcodeData, barcodeType)
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # print the barcode type and data to the terminal
    print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

