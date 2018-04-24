#Shantanu Singh
#Main class that returns the final output
from barcodeextract import Extract
from findcontours import Findcontours
from Nlp import Textprocessing
from resize import Resize
from rotate import Rotate
from rotated90 import Rotate90
import numpy as np
import argparse
import cv2
import PIL
import PIL.Image
import math
import imutils
import pytesseract
import os
from matplotlib import pyplot as plt
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
ext=Extract()
fc=Findcontours()
tp=Textprocessing()
rs=Resize()
rot=Rotate()
rot90=Rotate90()
class final:
    def main(self,Input_image):
        rotated=rot.rotateImage(Input_image)
        bar=ext.barcode(rotated)
        text=tp.nlp(bar)
        rotated90=rot90.rotateImage(Input_image)
        bar90=ext.barcode(rotated90)
        text90=tp.nlp(bar90)
        if(len(text)==0 and len(text90)==0):
            res=rs.rsize(Input_image)
            val=pytesseract.image_to_string(res)
            textfree=tp.nlp(val)
            if(len(textfree)>0):
                for i in textfree:
                    print(i)
            elif(len(textfree)==0):
                print("The image does not have a valid Tracking ID")
        elif(len(text)==0 and len(text90)>0):
            for j in text90:
                print((j))
        elif(len(text90)==0 and len(text)>0):
            for k in text:
                print(k)

image=input()#the accutal image
f=final()
f.main(image)
