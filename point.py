# USAGE
# python point.py --image real.jpg --path images/ --pointer point.png --pointer1 point1.png
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
ap.add_argument("-po", "--pointer", required=True, help="path to the input image")
ap.add_argument("-po1", "--pointer1", required=True, help="path to the input image")
args = vars(ap.parse_args())

_threshold_ = 0.9

def mathc_img(frame, Target, value):
    # image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    Target_gray = cv2.cvtColor(Target, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, Target_gray, cv2.TM_CCOEFF_NORMED)
    threshold = value
    loc = np.where(res >= threshold)
    is_match = 0
    for pt in zip(*loc[::-1]):
        # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
        cv2.circle(img_gray, pt, 50, (0, 255, 0), 2)  
        return pt, img_gray
#End

def cut_colums(point, point1, img_gray):
    # y, comprimento,   x, largura
    print( point[1] , 1600 , point[0] , point1[0] )
    tmp        = img_gray[ point[1] : 1600 , point[0] : point1[0]+100 ]
    
    return tmp
#End

def get_cicles(output, x, y, line):
    base = 172 #espaço entre letras

    cicle1, cicle2, cicle3, cicle4, cicle5 = (x, y), (x+172, y),(x+(base*2), y),(x+(base*3), y),(x+(base*4), y)
    cicles = [cicle1, cicle2, cicle3, cicle4, cicle5]
    key, answer = 0, -1
    for cicle in cicles:
        key = key+1
        #desenha circulo
        cv2.circle(output, cicle, 45 , (0, 255, 0), 1)
        #recorta circulo
        x, y = cicle
        r = 45

        crop_img1  = output[( y-r ):( y+r ), ( x-r ):( x+r )]
        cv2.imwrite('cut/'+str(line)+'_crop_img'+str(key)+'.png',crop_img1)
            
        n_white_pix0 = np.sum(crop_img1 == 253)
        n_white_pix1 = np.sum(crop_img1 == 254)
        n_white_pix2 = np.sum(crop_img1 == 255)
        n_white_pix3 = np.sum(crop_img1 == 252)
        n_white_pix4 = np.sum(crop_img1 == 251)
        n_white_pix5 = np.sum(crop_img1 == 250)
        n_white_pix6 = np.sum(crop_img1 == 249)
        n_white_pix7 = np.sum(crop_img1 == 248)
        n_white_pix  = np.sum((n_white_pix0,n_white_pix1,n_white_pix2,n_white_pix3,n_white_pix4,n_white_pix5,n_white_pix6,n_white_pix7))

        if(n_white_pix < 2000):
           answer = key

        print('Number of white pixels:', n_white_pix)
    
    print('Resposta marcada:', answer) 
    return output   
#End

def read(args):
    path      = args["path"]
    pre_image = cv2.imread(path+args["image"])
    pointer   = cv2.imread(path+args["pointer"])
    pointer1   = cv2.imread(path+args["pointer1"])
    print('Original Dimensions : ',pre_image.shape)

    image = pre_image.copy()

    point, img_gray = mathc_img( image, pointer, _threshold_ )
    cv2.imwrite('img_gray.png',img_gray)

    point1, img_gray = mathc_img( image, pointer1, _threshold_ )
    print(point, point1)

    output = cut_colums(point, point1, img_gray)    

    output = get_cicles(output, 755, 203, 1)
    output = get_cicles(output, 755, 350, 2)
    output = get_cicles(output, 755, 498, 3)

    cv2.imwrite('output.png',output)


if __name__ == "__main__":
  read(args)      