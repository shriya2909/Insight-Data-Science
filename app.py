# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 04:15:56 2020

@author: Shriya
"""

import PyPDF2
import streamlit  as st
import yake
from langdetect import detect
import iso_language_codes as ilc
from googletrans import Translator
from multi_rake import Rake


st.title("TL;DR")
st.header("Keyword Extraction for your scientific paper")

#Upload PDF 

uploaded_file = st.file_uploader("Choose scientific paper pdf", type="pdf")
if uploaded_file is not None:    
    # Load your PDF to text
    pdfReader  = PyPDF2.PdfFileReader(uploaded_file)
    num_pages = pdfReader.numPages
    count = 0
    pdftxt = ""
    #The while loop will read each page.
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        pdftxt += pageObj.extractText()
    txt = pdftxt
    st.write("File Upload Successful")
  
    lang = detect(txt)
    str1 = "Detected Origin of language : " + ilc.language_name(lang)
    st.write(str1)
    
    #----- RAKE 
    rake = Rake(language_code='es', max_words=1)
    rakekeywords = rake.apply(txt)

    if len(rakekeywords) > 25 :
        rakekeywords = rakekeywords[:25]
        
    #----- YAKE 
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 25
    
    custom_kw_extractor = yake.KeywordExtractor(lan=lang, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    yakekeywords = custom_kw_extractor.extract_keywords(txt)
    st.write("Extracting keywords now ...\n")
    
    translator = Translator()
    translated = translator.translate('Keywords', src='en', dest= lang)
    st.subheader(translated.text)
    
    for kw in yakekeywords:
        st.write(kw[1])
    tot_kw =[]
    for i in range(len(yakekeywords)):
        tot_kw.append(yakekeywords[i][0])
        
    for i in range(len(rakekeywords)):
        tot_kw.append(rakekeywords[i][0])
               
          
    freq = {} 
     for items in tot_kw: 
            freq[items] = tot_kw.count(items) 
            
    sorted_x = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)
    for kw in sorted_x:
        st.write(kw[1])
             
    



    

