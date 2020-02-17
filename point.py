# USAGE
# python point.py --img image
from imutils.perspective import four_point_transform
from imutils import contours
from pyzbar import pyzbar
import argparse
import imutils
import cv2, os, shutil

from lib_card import math_img, math_answer, cut_colums, get_circles, listdir, save_answer, cut_barcod

_threshold_ = 0.8
dirpath  =  'match/'
_DEBUG   = False

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
            answer_sensor = 2000
        else:
            move_to_fail(dirpath, pre_image_name)
            print("jump")
            break        

        image = pre_image.copy()
        
        point, img_gray  = math_img( image, pointer, _threshold_ )
        point1, img_gray = math_img( image, pointer1, _threshold_ )
        point2, img_gray = math_img( image, pointer2, _threshold_ )
        print(point, point1, point2)

        output = cut_colums(point, point1, point2, img_gray)    

        #if answer_sensor == 2000 :
        answer_img = output.copy()
        questions, output = math_answer(answer_img, 'points/7000/q')
        
        print(" questions : {}".format( len(questions) ))
        answers, debugs = [], []
        for j in range(len(questions)) :
            #get_cicles(output, X, Y , 200)
            y = questions[j][1] + 35
            if j <= 8 : # indice 9 a 10 questao
                x = questions[j][0] + 250
            else :
                x = questions[j][0] + 290 

            debugx, answer, output = get_circles(output, x , y , 45, j)
            answers.append(answer)
            debugs.append(debugx)

        #cv2.imwrite('cut/output.png',output)

        cod_bar  = pre_image.copy()
        decode, barcod  = cut_barcod(cod_bar, point)
        #break
       
        check_ok = False 
        for index in range(len(answers)) :
            if(answers[index] == -1) :
               check_ok = True

        if ( _DEBUG == True or check_ok == True or decode == ''):
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
