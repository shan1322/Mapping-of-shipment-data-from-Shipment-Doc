from cv2 import *
import cv2
import numpy as np
from findcontours import Findcontours
from resize import Resize
import PIL
import PIL.Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
rsiz=Resize()
cont=Findcontours()
file= open("data/bar.txt","w+")
class Extract:
    def barcode(self,image):
        barcodes=[]
        output=""
        contobj=cont.contours(image)
        rsizeobj=rsiz.rsize(image)
        number_of_contours=len(contobj)
        image = cv2.cvtColor(np.array(rsizeobj), cv2.COLOR_RGB2BGR) #PIL to cv
        for i in range(0,3):
            if(i>number_of_contours):
                break
            else:
                rect = cv2.minAreaRect(contobj[i])
                mask = np.zeros_like(image)      #mask for region surrounding barcode
                mask1 = np.ones(image.shape[:2], dtype="uint8") * 255
                x=int(rect[0][0])
                y=int(rect[0][1])
                if(rect[2]>=90 or rect[2]<=-90):         #width becomes the height and vice versa (obtuse)
                    w=int(rect[1][0]*0.5)    #0.5 times (vertically) because contour rect sometimes extends the barcode hence to avoid
                    h=int(rect[1][1])      #blacking out regions around the barcode
                else:
                    w=int(rect[1][0])
                    h=int(rect[1][1]*0.5)
                rect0=()
                rect0=rect0+ ((x,y),) + ((w,h),) + (rect[2],)  #rect0=region to be blacked out
                box1 = np.int0(cv2.boxPoints(rect0))
                x=int(rect[0][0])
                y=int(rect[0][1])
                if(rect[2]>=90 or rect[2]<=-90):
                    w=int(rect[1][0]*2)       #extending the boundaries (up-down)
                    h=int(rect[1][1])
                else:
                    w=int(rect[1][0])
                    h=int(rect[1][1]*2)
                rect1=()
                rect1=rect1+ ((x,y),) + ((w,h),) + (rect[2],)  #region to be cropped
                box = np.int0(cv2.boxPoints(rect1))
                cv2.drawContours(mask, [box], -1,  (255, 255, 255), -1)#scraping off barcode
                cv2.drawContours(mask1, [box1], -1,  0, -1)
                image = cv2.bitwise_and(image, image, mask=mask1)   #AND operation on image and mask1(blacked out region)
                #cropping to region surrounding barcode
                out = np.zeros_like(image)   #out has same dimensions as image but is completely black
                out[mask == 255] = image[mask == 255]   #drawing just mask(region surrounding barcode) on out
                (x, y, z) = np.where(mask == 255)
                (topx, topy, topz) = (np.min(x), np.min(y), np.min(z))
                (bottomx, bottomy, bottomz) = (np.max(x), np.max(y), np.max(z))
                out = out[topx:bottomx+1, topy:bottomy+1,]    #cropping to region surrounding barcode
                out = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)#grayscale
                cv2.imwrite('images/non'+str(i)+'.png',out)
                textv=pytesseract.image_to_string(out)
                barcodes.append(textv)
    
        for i in barcodes:
            output=output+i+" "
        return((output))#returns 5 image arryas
