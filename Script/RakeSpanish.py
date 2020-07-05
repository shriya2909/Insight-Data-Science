# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 20:48:48 2020

@author: Shriya
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 14:35:47 2020

@author: Shriya
"""
from multi_rake import Rake

txt= []
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

# Lowercase the text
lowertxt = [l.lower() for l in striptxt ]
print("LOWERCASE : \n")
print(lowertxt)
print("\n \n")

txt = ' '.join(map(str, lowertxt)) 



#Get gold keywords
key = []
with open ("C:/Users/Shriya/Downloads/cacic/keys/18572.key", 'r', encoding="utf8") as myfile:    
    for line in myfile:
        key.append(line)
 
stripkey= [l.strip('\n') for l in key ]
print(stripkey)
lowerkey = [l.lower() for l in stripkey ]
print("LOWERCASE : \n")
print(lowerkey)
print("\n \n")

print("Gold keywords : ", lowerkey)
rake = Rake(language_code='es', max_words=1)

keywords = rake.apply(txt)

print(keywords[:25])
print(len(keywords))

# number of top ranked keywords to evaluate


# evaluating

precision = 0
recall = 0

print(len(stripkey), 'manual keywords: ', lowerkey)
print('\nRAKE keywords:', keywords[:25])


## Removing null strings from stem_key - > 
gold_key = [i for i in lowerkey if i] 

num_manual_keywords = len(gold_key)
correct = 0

correct_key = []
for i in range(0,25):
    if keywords[i][0] in set(gold_key):
        correct_key.append(keywords[i][0])
        print(keywords[i][0])
        correct += 1
        
precision += correct/float(len(gold_key))
recall += correct/float(num_manual_keywords)
print('correct:', correct, 'out of', num_manual_keywords)


if correct != 0 :
    fmeasure = round(2*precision*recall/(precision + recall), 2)
else :
    fmeasure = 0 

print("Precision", precision, "Recall", recall, "F-Measure", fmeasure)

