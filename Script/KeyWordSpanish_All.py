# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 09:24:16 2020

@author: Shriya
"""
import os
import yake
from nltk.stem.snowball import SnowballStemmer

#Text Documents
txtdirectory ='C:/Users/Shriya/Desktop/Insight Data Science/Project/TL;DR/Evaluation/Data/cacic/docsutf8/'
#Key for the docs
keytxtdirectory = 'C:/Users/Shriya/Desktop/Insight Data Science/Project/TL;DR/Evaluation/Data/cacic/keys/'
count1 = 0 
count2 = 0 

#Current Language
lang = "english"
mystemmer=SnowballStemmer(lang, ignore_stopwords=True)
fmeasure = []
recall = []
precision = []  
    
for filename in os.listdir(txtdirectory):
    if filename.endswith(".txt"):
        count1 = count1 + 1
        txt = []
        txtfile = 'C:/Users/Shriya/Desktop/Insight Data Science/Project/TL;DR/Evaluation/Data/cacic/docsutf8/' + filename
        print(txtfile)
        with open (txtfile, 'r', encoding="utf8") as myfile:    
            for line in myfile:
                txt.append(line)
        print(count1)
        print("text files read")
        keyfile = 'C:/Users/Shriya/Desktop/Insight Data Science/Project/TL;DR/Evaluation/Data/cacic/keys/' + filename.replace(".txt", ".key")  
        count2 = count2 + 1
        print(keyfile)
        key = []
        stripkey = []
        with open (keyfile, 'r', encoding="utf8") as myfile:    
            for line in myfile:
                key.append(line)
        print(count2)
        print("key files read")
        stripkey= [l.strip('\n') for l in key ]
        print(stripkey)
        print("Current Gold keywords : ", stripkey)
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
        curr_precision = 0
        curr_recall = 0
        
        print(len(stripkey), 'manual keywords: ', stripkey)
        stem_key = []
        for key in stripkey:
            stem = mystemmer.stem(key)
            stem_key.append(stem)
        print(len(stem_key), 'stemmed manual keywords: ', stem_key)
        
        print('\nYAKE keywords:', keywords)
        
        stem_yake = []
        for i in range(len(keywords)):
            stem = mystemmer.stem(keywords[i][0])
            stem_yake.append(stem)
        print(len(stem_yake), 'stemmed yake keywords: ', stem_yake)
        
        ## Removing null strings from stem_key - > 
        stem_key = [i for i in stem_key if i] 
        
        num_manual_keywords = len(stem_key)
        correct = 0
        
        correct_key = []
        for i in range(0,len(stem_yake)):
            if stem_yake[i] in set(stem_key):
                correct_key.append(keywords[i])
                print(keywords[i][0])
                correct += 1
                
        curr_precision += correct/float(len(stem_key))
        curr_recall += correct/float(len(keywords))
        print('correct:', correct, 'out of', num_manual_keywords)

        
        if correct != 0 :
            curr_fmeasure = round(2*curr_precision*curr_recall/(curr_precision + curr_recall), 2)
        else :
            curr_fmeasure = 0 
            
        recall.append(curr_recall)
        precision.append(curr_precision)
        fmeasure.append(curr_fmeasure)



avg_fmeasure = sum(fmeasure)/ len(fmeasure) 
print("Average F-Measure :")
print(avg_fmeasure)

print(max(fmeasure))
print(max(precision))
print(max(recall))