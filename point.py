# USAGE
# python point.py --img image
from imutils.perspective import four_point_transform
from imutils import contours
from pyzbar import pyzbar
import argparse
import imutils
import cv2, os

from lib_card import mathc_img, cut_colums, get_cicles, listdir, save_answer, cut_barcod

_threshold_ = 0.8
dirpath  =  'match/'

ap = argparse.ArgumentParser()
ap.add_argument("-img", "--img", required=False, help="path to the input image")
args = vars(ap.parse_args())

def read(args):  
    if(args["img"]): 
        entries   = [args["img"]]
    else:
        entries = listdir(dirpath)
   
    print(entries) 

    for pre_image_name in entries:
        pre_image = cv2.imread(dirpath+pre_image_name)   
        print(pre_image_name,' : ',pre_image.shape)   
        shape = 0  
        
        if(pre_image.shape[0] > 6000):
            pointer   = cv2.imread('points/7000/point.png')
            pointer1  = cv2.imread('points/7000/point1.png')
            pointer2  = cv2.imread('points/7000/point2.png')  
            answer_sensor = 7000

        elif(pre_image.shape[0] < 6000 and pre_image.shape[0] > 4000):
            #move arquivo fora do padrao para fora
            os.rename(dirpath+pre_image_name, 'fail/'+pre_image_name)
            print("jump")
            continue 

            ## criar nova mascara
            pointer   = cv2.imread('points/4000/point.png')
            pointer1  = cv2.imread('points/4000/point1.png')   
            pointer2  = cv2.imread('points/4000/point2.png')  
            answer_sensor = 2000

        else:
            #move arquivo fora do padrao para fora
            os.rename(dirpath+pre_image_name, 'fail/'+pre_image_name)
            print("jump")
            continue 

            ## criar nova mascara
            pointer   = cv2.imread('points/7000/point.png')
            pointer1  = cv2.imread('points/7000/point1.png')
            pointer2  = cv2.imread('points/7000/point2.png')  
            answer_sensor = 7000

        image = pre_image.copy()
        
        point, img_gray = mathc_img( image, pointer, _threshold_ )
        cv2.imwrite('cut/img_gray.png',img_gray)

        point1, img_gray = mathc_img( image, pointer1, _threshold_ )
        point2, img_gray = mathc_img( image, pointer2, _threshold_ )
        print(point, point1, point2)

        output = cut_colums(point, point1, point2, img_gray)    

        '''
        (output, 755, 203, 172, 1)
        1)imagem crop
        2)posio X
        3)posio Y
        4)espao entre as bolinhas
        5)linha das bolinhas
        '''
        calc   = int((point1[0] - point[0])/25) #172
        y =  int( ((output.shape[0] /2)/2)/2 ) #x - 80

        output, answer1 = get_cicles(output, y*3     , calc, 1, answer_sensor) #203
        output, answer2 = get_cicles(output, y*5     , calc, 2, answer_sensor) #350
        output, answer3 = get_cicles(output, y*7     , calc, 3, answer_sensor) #498

        cod_bar  = pre_image.copy()
        decode   = cut_barcod(cod_bar, point)
        #break

        save_answer(pre_image_name, decode, answer1, answer2, answer3)

    cv2.imwrite('cut/output.png',output)

if __name__ == "__main__":
  read(args)      
