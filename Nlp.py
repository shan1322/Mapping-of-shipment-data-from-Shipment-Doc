#Shantanu Singh
#Tejpala
#Shiva
#Class extracts out the barcode from the ocr of document
import pandas as pd
from collections import Counter
from nltk import FreqDist, word_tokenize
import nltk
import re
import tracking_url
trackid8=[]
class Textprocessing:
    def nlp(self,line):
        trackid=[]
        cardinal=[]
        alpha=[]
        alphanum=[]
        lines=((line).upper().split('\n'))
        testspace='^[a-zA-Z0-9]{4}[ ]{1}[a-zA-Z0-9]{4}[ ]{1}[a-zA-Z0-9]{4}'
        for i in lines:
            wt=word_tokenize(i)
            words=(nltk.pos_tag(wt))
            for j in range(0,len(words)):
                if(words[j][1]=='CD'):
                    cardinal.append(words[j][0])
                elif(re.match("^[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)?$", words[j][0])):
                    alphanum.append(words[j][0])
                if(words[j][0].isalpha()):
                    alpha.append(words[j][0])
                if(re.match(testspace,words[j][0])):
                    print(words[j][0])
                    alphanum.append((words[j][0]).replace(" ",""))
        test=set(alphanum)-set(alpha)
        trackid=list(set().union(test,cardinal))
        trackid8=[]
        for i in trackid:
            if(len(i)>8):
                trackid8.append(i)
        df = pd.read_excel('data/regx.xlsx', sheetname=0) # can also index sheet by name or fetch all sheets
        validation1= df['pass'].tolist()
        validid=[]
        for i in trackid8:
            for j in validation1:
                if(re.match(j,i)):
                    validid.append(i)
        for i in trackid8:
            match = tracking_url.guess_carrier(i)
            if match is None:
                pass
            else:
                validid.append(i)
        return(list(set(validid)))
