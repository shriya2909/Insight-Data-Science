# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 09:09:32 2020

@author: Shriya
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 16:06:43 2020

@author: Shriya
"""
import yake
import re 
from nltk.stem.snowball import SnowballStemmer

lang = "spanish"
mystemmer=SnowballStemmer(lang, ignore_stopwords=True)


#Flags  
intro_flag = 0 
kw_flag = 0
abstract_flag = 0 

#Introduction Check
pattern1 = re.compile("Introduction", re.IGNORECASE)
pattern2 = re.compile("I NTRODUCTION", re.IGNORECASE)
txt = []
# Extract content only before Introduction if there is one, Otherwise extract all 
with open ("C:/Users/Shriya/Downloads/cacic/docsutf8/18572.txt", 'r', encoding="utf8") as myfile:    
    for line in myfile:
#        if pattern1.search(line) != None or pattern2.search(line) != None:  
#            # If an Introduction is found 
#            intro_flag = 1
#            break
        txt.append(line)
print(txt)
striptxt = [l.strip('\n') for l in txt ]
print(striptxt)
#Get gold keywords
key = []
with open ("C:/Users/Shriya/Downloads/cacic/keys/18572.key", 'r', encoding="utf8") as myfile:    
    for line in myfile:
        key.append(line)
 
stripkey= [l.strip('\n') for l in key ]
print(stripkey)
print("Gold keywords : ", stripkey)
# Check to see if keywords is present in any of the objects in the list 
pattern3 = re.compile("Keywords", re.IGNORECASE)
pattern4 = re.compile("Key words", re.IGNORECASE)
pattern5 =  re.compile("Index Terms", re.IGNORECASE)


for line in txt:
    if (pattern3.search(line) != None or pattern4.search(line) != None or pattern5.search(line) != None) and intro_flag == 1 :     
        # If a match is found for keywords in doc and it is before Introduction
        print("Found Keywords in PDF")    
        print(line)
        kw_flag = 1
        

# No Keywords found in PDF itself 

if kw_flag == 0 :
    
    # Check if we can find Abstract if we have found already Introduction
    pattern6 =  re.compile("Abstract", re.IGNORECASE)
    fTxt = []
    i = 0 
    for i in range(0,len(txt)):
        if pattern6.search(txt[i]) != None and intro_flag == 1 :     
        # If Abstract is found before Introduction
            print("Found Abstract") 
            abstract_flag = 1
            break
    if abstract_flag == 1 :
        fTxt = txt[i+1:]
        print(fTxt)
    
    if abstract_flag == 1 : 
        txt = ' '.join(map(str, fTxt))      
        
    else :
        txt = ' '.join(map(str, txt))      
        

    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 25
    
    custom_kw_extractor = yake.KeywordExtractor(lan=lang, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(txt)
    print("Extracting keywords now ...\n")
    print("Keywords : \n ")
    for kw in keywords:
        print(kw)


# Add code to evaluate performance



# number of top ranked keywords to evaluate
top = 25

# evaluating

precision = 0
recall = 0

print(len(stripkey), 'manual keywords: ', stripkey)
stem_key = []
for key in stripkey:
    stem = mystemmer.stem(key)
    stem_key.append(stem)
print(len(stem_key), 'stemmed manual keywords: ', stem_key)

print('\nYAKE keywords:', keywords)

stem_yake = []
for i in range(top):
    stem = mystemmer.stem(keywords[i][0])
    stem_yake.append(stem)
print(len(stem_yake), 'stemmed yake keywords: ', stem_yake)

## Removing null strings from stem_key - > 
stem_key = [i for i in stem_key if i] 

num_manual_keywords = len(stem_key)
correct = 0

correct_key = []
for i in range(0,max(top, len(stem_key))):
    if stem_yake[i] in set(stem_key):
        correct_key.append(keywords[i])
        print(keywords[i][0])
        correct += 1
        
precision += correct/float(len(stem_key))
recall += correct/float(num_manual_keywords)
print('correct:', correct, 'out of', num_manual_keywords)


if correct != 0 :
    fmeasure = round(2*precision*recall/(precision + recall), 2)
else :
    fmeasure = 0 

print("Precision", precision, "Recall", recall, "F-Measure", fmeasure)
