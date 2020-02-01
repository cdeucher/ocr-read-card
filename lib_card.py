import numpy as np
import cv2, os
import os.path
from pyzbar import pyzbar

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
    # y, altura,   x, largura
    print('cut comuns:', point[1] , 1600 , point[0] , point1[0] )
    tmp = img_gray[ point[1] : 1600 , point[0] : point1[0]+100 ]
    
    return tmp
#End

def sum_pixel(crop_img, start, end):
    n = 0
    for number in range(start, end):
        n = n + np.sum(crop_img == number)

    return n    
#End

def get_cicles(output, x, y, base, line):
    #base = 172 #espaço entre letras

    cicle1, cicle2, cicle3, cicle4, cicle5 = (x, y), (x+base, y),(x+(base*2), y),(x+(base*3), y),(x+(base*4), y)
    cicles = [cicle1, cicle2, cicle3, cicle4, cicle5]
    key, answer, count = 0, -1, 99999
    for cicle in cicles:
        key = key+1
        #desenha circulo
        cv2.circle(output, cicle, 45 , (0, 255, 0), 1)
        #recorta circulo
        x, y = cicle
        r = 45

        crop_img1  = output[( y-r ):( y+r ), ( x-r ):( x+r )]
        cv2.imwrite('cut/'+str(line)+'_crop_img'+str(key)+'.png',crop_img1)
        
        n_white_pix = sum_pixel(crop_img1, 240, 260)
        print('White pixels:', n_white_pix)

        if(n_white_pix < count and n_white_pix < 3000):
           count  = n_white_pix
           answer = key
           print( 'check', count, answer )        
    
    print('Resposta marcada:', answer) 
    print('-----------------------------------------------') 
    return output, answer   
#End

def listdir(dirpath):

    entries = os.listdir(dirpath)
    return entries
#End    

def fileExists(file):
    if os.path.isfile(file):
        return True
    else:
        return False
#End

def save_answer(pre_image_name, decode, answer1, answer2, answer3):
    if not fileExists("answers.txt") :
        f= open("answers.txt","w+")
    else:
        f= open("answers.txt","a+")

    f.write(pre_image_name+';'+decode+';'+str(answer1)+';'+str(answer2)+';'+str(answer3)+ "\n")
    f.close() 
#End    

#https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
def cut_barcod(image, point):
    y, heigth, x, width = 10, point[1], 10, 1800
    # y, altura,   x, largura
    #print( y, heigth, x, width )
    tmp = image[ y: heigth, x: width ]

    cv2.imwrite('cut/bar_cod.jpg',tmp) 

    decode = barcod(tmp)

    return decode
#End

def barcod(image):
    barcodes = pyzbar.decode(image)
    barcodeData = ''
    #print('barcodes',barcodes)
    if not barcodes:
        mask = cv2.inRange(image,(0,0,0),(200,200,200))
        thresholded = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
        inverted = 255-thresholded # black-in-white

        barcodes = pyzbar.decode(inverted)
        print('fliped barcodes')#,barcodes)

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

    return barcodeData    
#End   