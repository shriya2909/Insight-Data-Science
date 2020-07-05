# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 08:07:03 2020

@author: Shriya
"""

import yake
import re 
import nltk 
from nltk.stem.snowball import SnowballStemmer
import string
from string import digits
from nltk.corpus import stopwords

lang = "spanish"
mystemmer=SnowballStemmer(lang)


#from googletrans import Translator
#
#translator = Translator()
#Intro_es = translator.translate('Introduction', src='en',dest='es')

#Flags  
intro_flag = 0 
kw_flag = 0
abstract_flag = 0 

#Introduction Check
pattern1 = re.compile("Introduction", re.IGNORECASE)
pattern2 = re.compile("I NTRODUCTION", re.IGNORECASE)
txt = []

# Extract content only before Introduction if there is one, Otherwise extract all 
with open ("C:/Users/Shriya/Downloads/cacic/docsutf8/18688.txt", 'r', encoding="utf8") as myfile:    
    for line in myfile:
        if pattern1.search(line) != None or pattern2.search(line) != None:  
            # If an Introduction is found 
            intro_flag = 1
            break
        txt.append(line)
print("ORIGINAL : \n")
print(txt)
print("\n \n")

# Pre-processing 

# Remove newlines from text
striptxt = [l.strip('\n') for l in txt ]
print("STRIP : \n")
print(striptxt)
print("\n \n")

# Lowercase the text
lowertxt = [l.lower() for l in striptxt ]
print("LOWERCASE : \n")
print(lowertxt)
print("\n \n")

# Remove punctuation from text
txt_no_punct = [l.translate(str.maketrans('', '', string.punctuation)) for l in lowertxt ]
print("NO PUNCTUATION : \n")
print(txt_no_punct)
print("\n \n")

# Remove digits from text
txt_no_digit = [l.translate(str.maketrans('', '', digits)) for l in txt_no_punct ]
print("NO DIGIT : \n")
print(txt_no_digit )
print("\n \n")

# Tokenize the text into words
tokenizer = nltk.RegexpTokenizer(r"\w+")
new_words = [tokenizer.tokenize(l) for l in txt_no_digit  ]
print("TOKENIZED : \n")
print(new_words)
print("\n \n")


# Remove stop words from text
#actual_words = []
#for word in new_words:
#    if word not in stopwords.words(lang):
#        actual_words.append(word)
#print("STOP WORDS REMOVED : \n")
#print(actual_words)
#print("\n \n")


# Stem words in list of tokenized words
stems = []
for sent in new_words:
    for word in sent:
        stem = mystemmer.stem(word)
        stems.append(stem)
print("STEMMED WORDS: \n")
print(stems)
print("\n \n")


txt = ' '.join(map(str, stems))

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


key = []
with open ("C:/Users/Shriya/Downloads/cacic/keys/18688.key", 'r', encoding="utf8") as myfile:    
    for line in myfile:
        key.append(line)
 
stripkey= [l.strip('\n') for l in key ]
print(stripkey)
print("Gold keywords : ", stripkey)


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

