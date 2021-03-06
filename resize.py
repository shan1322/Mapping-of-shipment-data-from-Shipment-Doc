#Shantanu Singh
# Class reizes the image to get proper output from tesseract
import PIL.Image
import PIL
class Resize:
    def rsize(self,image):
        try:
            im = PIL.Image.open(image)
        except:
            im =image
        x,y=im.size
        while x<1800 or y<1800:
            x*=1.15
            y*=1.15
        im=im.resize((int(x),int(y)), PIL.Image.ANTIALIAS)
        return im #returning resized image object
