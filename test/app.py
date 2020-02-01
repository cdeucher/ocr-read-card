# USAGE
# python app.py --image prova.jpg --path images/
from imutils.perspective import four_point_transform
from imutils import contours
from pyzbar import pyzbar
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
ap.add_argument("-p", "--path", required=True, help="path to the input image")
args = vars(ap.parse_args())


def barcod(image):
    barcodes = pyzbar.decode(image)

    print(barcodes)

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

#End    
def find(image, files):
    #w, h = template.shape[::-1]
    #cv2.imwrite('tmp.png',img_gray) 
    point1 = cv2.matchTemplate(image, files[0] ,cv2.TM_CCOEFF_NORMED)
    point2 = cv2.matchTemplate(image, files[1] ,cv2.TM_CCOEFF_NORMED)
    point3 = cv2.matchTemplate(image, files[2] ,cv2.TM_CCOEFF_NORMED)        

    threshold = 0.8
    loc1 = np.where( point1 >= threshold)   
    loc2 = np.where( point2 >= threshold)
    loc3 = np.where( point3 >= threshold)

    for pt in zip(*loc1[::-1]):
        start = pt 
    for pt in zip(*loc2[::-1]):
        width = pt        
    for pt in zip(*loc3[::-1]):
        height = pt
 

    return start, width, height
#End

#https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
def cut_barcod(image):
    w,h,yy,xx      = 550, 130, 110, 30
    img_proc   = image.copy()
    # y, comprimento,   x, largura
    tmp        = img_proc[ p[0][1]- yy : h , p[0][0]- xx : w ]
    #cv2.imwrite('tmp.png',tmp) 
    return tmp
#End

def get_cicles(output, size):
    base = int(round(size[1]/size[0], 1))
    calc = 10

    row1_yy = ( base*5 ) + 4
    row1_xx = ( base*12 ) 
    cicle1, cicle2, cicle3, cicle4, cicle5 = (row1_xx, row1_yy), (125, row1_yy), (171, row1_yy), (216, row1_yy), (261, row1_yy)
    cicles = [cicle1, cicle2, cicle3, cicle4, cicle5]
    key, answer = 0, -1
    for cicle in cicles:
        key = key+1
        #desenha circulo
        cv2.circle(output, cicle,( base+2 ), (0, 255, 0), 1)
        #recorta circulo
        x, y = cicle
        r = 10
        crop_img1  = output[( y-r ):(y+r), ( x-r ):(x+r)]
            
        gray1 = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)

        n_white_pix = np.sum(gray1 == 255)

        if(n_white_pix < 20):
           answer = key

        print('Number of white pixels:', n_white_pix)
    
    cv2.imwrite('res.png',output)
    print('Resposta marcada:', answer)    
#End

def resize(img):
    scale_percent = 90 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    return resized
#End

def resize_scale(pre_image, path):
    start = (0,0)
    point1 = cv2.imread(path+'point2.png')
    point = cv2.matchTemplate(pre_image, point1 ,cv2.TM_CCOEFF_NORMED)
    loc = np.where( point >= 0.7)   
    for pt in zip(*loc[::-1]):
        start = pt 

    return start
#End

def read(args):
    path      = args["path"]
    pre_image = cv2.imread(path+args["image"])
    print('Original Dimensions : ',pre_image.shape)

    image = pre_image.copy()



    start = resize_scale(pre_image, path)
    count = 0
    while count < 10 and start[0] <= 0:
        count = count+1
        image  = resize(image)
        print('Resizing : ',image.shape)    
        start = resize_scale(image, path)
        print('start : ',start) 

    print('Resize Dimensions : ',image.shape)    
   
    cv2.imwrite('tmp.png',image) 

    files    = []    
    files.append(cv2.imread(path+'point1.png'))
    files.append(cv2.imread(path+'point2.png'))
    files.append(cv2.imread(path+'point3.png'))
    
    cod_bar  = image.copy()

    start, width, height = find(image, files)
    print(start, width, height)

    output = cut_colums(start, width, height, image)

    print('output', output.shape )

    get_cicles(output, output.shape)



    '''
    bar = cut_barcod(output)    
    barcod(bar)
    '''
#End


if __name__ == "__main__":
  read(args)  