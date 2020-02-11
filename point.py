# USAGE
# python point.py --img image
from imutils.perspective import four_point_transform
from imutils import contours
from pyzbar import pyzbar
import argparse
import imutils
import cv2, os, shutil

from lib_card import math_img, math_answer, cut_colums, get_cicles, listdir, save_answer, cut_barcod

_threshold_ = 0.8
dirpath  =  'match/'
_DEBUG   = True

ap = argparse.ArgumentParser()
ap.add_argument("-img", "--img", required=False, help="path to the input image")
args = vars(ap.parse_args())

def move_to_fail(dirpath, pre_image_name):
    #move arquivo fora do padrao para fora
    os.rename(dirpath+pre_image_name, 'fail/'+pre_image_name)
    shutil.move("cut", 'fail/'+pre_image_name+'_folder')
    os.mkdir("cut")
#End    
def read(args):  
    if(args["img"]): 
        entries   = [args["img"]]
    else:
        entries = listdir(dirpath)
   
    print(entries) 

    for pre_image_name in entries:
        print(dirpath+pre_image_name)
        pre_image = cv2.imread(dirpath+pre_image_name)   
        print(pre_image_name,' : ',pre_image.shape)   
        shape = 0  
        
        if(pre_image.shape[0] > 6000):
            pointer   = cv2.imread('points/7000/point.png')
            pointer1  = cv2.imread('points/7000/point1.png')
            pointer2  = cv2.imread('points/7000/point2.png')  
            list1     = cv2.imread('points/7000/answer1.png')
            answer_sensor = 2000

        elif(pre_image.shape[0] < 6000 and pre_image.shape[0] > 4000):
            pointer   = cv2.imread('points/4000/point.png')
            pointer1  = cv2.imread('points/4000/point1.png')   
            pointer2  = cv2.imread('points/4000/point2.png')  
            answer_sensor = 700

        else:
            move_to_fail(dirpath, pre_image_name)
            print("jump")
            continue             

        image = pre_image.copy()
        
        point, img_gray  = math_img( image, pointer, _threshold_ )
        point1, img_gray = math_img( image, pointer1, _threshold_ )
        point2, img_gray = math_img( image, pointer2, _threshold_ )
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
        if answer_sensor == 2000 :
            #answer_img = output.copy()
            #answers, output = math_answer(answer_img, list1)
            #print(" answers : {}".format(answers))

            calc   = int((point1[0] - point[0])/25) #172
            y =  int( (((((output.shape[0] /2)/2)/2)/2)/2)/2 ) #x - 80

            ## 1 colum
            x =  int( ((((((output.shape[1] /2)/2)/2)/2)/2)/2) )  
            xx = int(x*11)

            debug1, answer1 = get_cicles(output, y*11   , x, xx  , calc, 1, answer_sensor) 
            debug2, answer2 = get_cicles(output, y*19   , x, xx  , calc, 2, answer_sensor) 
            debug3, answer3 = get_cicles(output, y*27   , x, xx  , calc, 3, answer_sensor) 
            debug4, answer4 = get_cicles(output, y*35   , x, xx  , calc, 4, answer_sensor) 
            debug5, answer5 = get_cicles(output, y*43   , x, xx  , calc, 5, answer_sensor) 
            debug6, answer6 = get_cicles(output, y*51   , x, xx  , calc, 6, answer_sensor) 

            ## 2 colum
            x =  int( ((((((output.shape[1] /2)/2)/2)/2)/2)/2) )  
            xx = int(x*29)

            debug7 , answer7  = get_cicles(output, y*11   , x, xx  , calc, 7, answer_sensor) 
            debug8 , answer8  = get_cicles(output, y*19   , x, xx  , calc, 8, answer_sensor) 
            debug9 , answer9  = get_cicles(output, y*27   , x, xx  , calc, 9, answer_sensor) 
            debug10, answer10 = get_cicles(output, y*35   , x, xx  , calc,10, answer_sensor) 
            debug11, answer11 = get_cicles(output, y*43   , x, xx  , calc,11, answer_sensor) 
            debug12, answer12 = get_cicles(output, y*51   , x, xx  , calc,12, answer_sensor) 

            ## 3 colum
            x =  int( (((((((output.shape[1] /2)/2)/2)/2)/2)/2)/2) )  
            xx = int(x*96)

            debug13 , answer13  = get_cicles(output, y*11   , x, xx  , calc, 13, answer_sensor) 
            debug14 , answer14  = get_cicles(output, y*19   , x, xx  , calc, 14, answer_sensor) 
            debug15 , answer15  = get_cicles(output, y*27   , x, xx  , calc, 15, answer_sensor) 
            debug16 , answer16  = get_cicles(output, y*35   , x, xx  , calc, 16, answer_sensor) 

        elif answer_sensor == 700 :
            calc   = int((point1[0] - point[0])/25) #172
            y =  int( ((output.shape[0] /2)/2)/2 ) #x - 80

            debug1, answer1 = get_cicles(output, y*2     , calc, 1, answer_sensor) #203
            debug2, answer2 = get_cicles(output, y*3     , calc, 2, answer_sensor) #350
            debug3, answer3 = get_cicles(output, y*4     , calc, 3, answer_sensor) #498
        #EndiF

        debugs = [debug1, debug2, debug3, debug4, debug5, debug6, debug7, debug8, debug9, debug10, debug11, debug12, debug13, debug14, debug15, debug16]
        answers = [answer1, answer2, answer3, answer4, answer5, answer6, answer7, answer8, answer9, answer10, answer11, answer12, answer13, answer14, answer15, answer16]

        cod_bar  = pre_image.copy()
        decode, barcod  = cut_barcod(cod_bar, point)
        #break
       
        check_ok = False 
        for index in range(len(answers)) :
            if(answers[index] == -1) :
               check_ok = True

        if ( _DEBUG == True or check_ok == True ):
            debug(img_gray, output, barcod, debugs)
            #move_to_fail(dirpath, pre_image_name) 
        else :    
            save_answer(pre_image_name, decode, answers)
#End

def debug(img_gray, output, barcod, debugs):
    cv2.imwrite('cut/img_gray.png',img_gray)
    cv2.imwrite('cut/output.png',output)
    cv2.imwrite('cut/bar_cod.jpg',barcod)

    for j in range(len(debugs)) :
        for i in range(len(debugs[j])) :
            cv2.imwrite('cut/line_'+str(j)+'_'+str(i)+'.png',debugs[j][i])

#End

if __name__ == "__main__":
  read(args)      
