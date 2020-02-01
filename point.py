# USAGE
# python point.py --image real.jpg --path points/ --pointer point.png --pointer1 point1.png
from imutils.perspective import four_point_transform
from imutils import contours
from pyzbar import pyzbar
import argparse
import imutils
import cv2, os

from lib_card import mathc_img, cut_colums, get_cicles, listdir, save_answer, cut_barcod

_threshold_ = 0.9
dirpath  =  'match/'

ap = argparse.ArgumentParser()
ap.add_argument("-po", "--pointer", required=True, help="path to the input image")
ap.add_argument("-po1", "--pointer1", required=True, help="path to the input image")
args = vars(ap.parse_args())

def read(args):
    pointer   = cv2.imread('points/'+args["pointer"])
    pointer1  = cv2.imread('points/'+args["pointer1"])

    entries = listdir(dirpath)

    print(entries) 

    for pre_image_name in entries:
        pre_image = cv2.imread(dirpath+pre_image_name)   
        print(pre_image_name,' : ',pre_image.shape)     

        image = pre_image.copy()

        point, img_gray = mathc_img( image, pointer, _threshold_ )
        cv2.imwrite('cut/img_gray.png',img_gray)

        point1, img_gray = mathc_img( image, pointer1, _threshold_ )
        print(point, point1)

        output = cut_colums(point, point1, img_gray)    

        '''
        (output, 755, 203, 172, 1)
        1)imagem crop
        2)posição X
        3)posição Y
        4)espaço entre as bolinhas
        5)linha das bolinhas
        '''
        calc   = int((point1[0] - point[0])/25) #172

        output, answer1 = get_cicles(output, 760, 203, calc, 1)
        output, answer2 = get_cicles(output, 760, 350, calc, 2)
        output, answer3 = get_cicles(output, 760, 498, calc, 3)

        cod_bar  = pre_image.copy()
        decode   = cut_barcod(cod_bar, point)
        #break

        save_answer(pre_image_name, decode, answer1, answer2, answer3)

    cv2.imwrite('cut/output.png',output)

if __name__ == "__main__":
  read(args)      