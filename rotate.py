#Agranya Pratap Singh
#Rotated image output
import imutils
import PIL
from PIL import Image
import cv2
import numpy as np
import math
from findcontours import Findcontours
from resize import Resize
findcont=Findcontours()
rsiz=Resize()
class Rotate:
    def rotatedRectWithMaxArea(self,w, h, angle):
        #largest rectangle that can cover the image excluding black borders
        if(w <= 0 or h <= 0):
            return 0,0
        width_is_longer=w>=h
        side_long, side_short = (w,h) if width_is_longer else (h,w)      #storing the longer and shorter sides
        sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
        if(side_short <= 2.*sin_a*cos_a*side_long or abs(sin_a-cos_a) < 1e-10):
            x = 0.5*side_short
            wr,hr = (x/sin_a,x/cos_a) if width_is_longer else (x/cos_a,x/sin_a)
        else:
            cos_2a = cos_a*cos_a - sin_a*sin_a
            wr,hr = (w*cos_a - h*sin_a)/cos_2a, (h*cos_a - w*sin_a)/cos_2a
        return wr,hr
    def rotate_max_area(self,image, angle):         #crops rotated image to remove black borders
        wr, hr = self.rotatedRectWithMaxArea(image.shape[1], image.shape[0], math.radians(angle))  #getting dimensions of 'largest rect' excluding
        rotated = imutils.rotate_bound(image, angle)   #rotating the image
        h, w, _ = rotated.shape
        y1 = h//2 - int(hr/2)
        y2 = y1 + int(hr)
        x1 = w//2 - int(wr/2)
        x2 = x1 + int(wr)
        return rotated[y1:y2, x1:x2]          #cropping to just the 'largest rect'
    def rotateImage(self,image):
        c=findcont.contours(image)[0]
        rsobj=rsiz.rsize(image)
        image = cv2.cvtColor(np.array(rsobj), cv2.COLOR_RGB2BGR)   #PIL to cv2 image
        rect = cv2.minAreaRect(c)
        box = np.int0(cv2.boxPoints(rect))
        v=(box[0][0],box[1][0],box[1][1],box[0][1])  #box[0][0] & box[1][0] are boundaries (x axis) box[1][1] & box[0][1] (y axis)
        m=0
        if not(v[3]==v[2]):  #m=infinite if v[3]==v[2]
            m=abs((v[1]-v[0])/((v[3]-v[2])*1.0))     #slope of box==>slope of image
        rot=(math.degrees(math.atan(m)))
        if not(rot==0 or m==0):   #providing padding only if image is tilted
            old_im= Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))   #cv2 to PIL
            old_size = old_im.size
            ns=int(1.3*math.sqrt((old_size[0]**2 + old_size[1]**2))) #square image with dimensions as 1.25 times diagonal of old image
            #providing white padding so that image doesnt get cropped after rotation
            new_size=(ns, ns)
            new_im = Image.new("RGB", new_size, color=(255, 255, 255))  #new image (completely white) with new_size
            new_im.paste(old_im, (int((new_size[0]-old_size[0])/2), int((new_size[1]-old_size[1])/2))) #pasting old image at the center
            image = cv2.cvtColor(np.array(new_im), cv2.COLOR_RGB2BGR)
        if (rot>0 and rot<90) or (rot>180 and rot<270):
            image=self.rotate_max_area(image, rot)
        else:
            image=self.rotate_max_area(image, 360-rot)
        image= Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))    #cv2 to PIL
        return image
