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
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 25
    
    custom_kw_extractor = yake.KeywordExtractor(lan=lang, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(txt)
    st.write("Extracting keywords now ...\n")
    
    translator = Translator()
    translated = translator.translate('Keywords', src='en', dest= lang)
    st.subheader(translated.text)
    
    for kw in keywords:
        st.write(kw)

#    th = TextHighlighter(max_ngram_size = 3, highlight_pre = "<span class='my_class' >", highlight_post= "</span>")
#    st.markdown(th.highlight(txt, keywords),unsafe_allow_html  = True)

    

