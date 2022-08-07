#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import numpy as np
import re
from PyPDF2 import PdfReader
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


# In[3]:


import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns


# In[4]:


def main():
    """LEGAL TEXT SUMMARIZATION """
    activities = ["LEGAL TEXT SUMMARY"]
    choice = st.sidebar.selectbox("Select Activities",activities)

    if choice == 'LEGAL TEXT SUMMARY':
        st.subheader("SUMMARIZATION PROCESS BEGINS")

        data = st.file_uploader("Upload legal document", type=["pdf"])
        if data is not None:
            reader = PdfReader(data)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            f=open('xxx.txt','w')
            f.write(text)
            f.close()
            with open('xxx.txt') as f:
                clean_cont = f.read().splitlines()
            legal_doc = clean_cont
#               PREPROCESSING DOCUMENT
            temp = ""
            for eachDocument in legal_doc[:]:
                eachDocument = re.sub(r'(\d\d\d|\d\d|\d)\.\s', ' ', eachDocument)#removes the paragraph lables 1. or 2. etc.
                eachDocument = re.sub(r'(?<=[a-zA-Z])\.(?=\d)', '', eachDocument)#removes dot(.) i.e File No.1063
                eachDocument = re.sub(r'(?<=\d|[a-zA-Z])\.(?=\s[\da-z])', ' ', eachDocument)#to remove the ending dot of abbr
                eachDocument = re.sub(r'(?<=\d|[a-zA-Z])\.(?=\s?[\!\"\#\$\%\&\'\(\)\*\+\,\-\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~])', '', eachDocument)#to remove the ending dot of abbr
                eachDocument = re.sub(r'(?<!\.)[\!\"\#\$\%\&\'\(\)\*\+\,\-\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]', ' ', eachDocument)#removes the other punctuations
                temp = temp +''+eachDocument
            documents = []
            temp = temp.replace("  "," ")
            documents = temp.replace(" ","",1)    
            activities2 = ["WORD COUNT OF ORIGINAL DOCUMENT","SHOW PROCESSED DOCUMENT","PROCEED TO SUMMARY"]
            choice2 = st.sidebar.selectbox("Select Activities",activities)
            if choice2 == 'WORD COUNT OF ORIGINAL DOCUMENT':
                original_length = len(data.split())
                st.write(original_length)
            if choice2 == 'WORD COUNT OF ORIGINAL DOCUMENT':
                st.write(data)
            if choice2 == 'PROCEED TO SUMMARY':
                def summarize(text, per):
                    nlp = spacy.load('en_core_web_sm')
                    doc= nlp(text)
                    tokens=[token.text for token in doc]
                    word_frequencies={}
                    for word in doc:
                        if word.text.lower() not in list(STOP_WORDS):
                            if word.text.lower() not in punctuation:
                                if word.text not in word_frequencies.keys():
                                    word_frequencies[word.text] = 1
                                else:
                                    word_frequencies[word.text] += 1
                    max_frequency=max(word_frequencies.values())
                    for word in word_frequencies.keys():
                        word_frequencies[word]=word_frequencies[word]/max_frequency
                    sentence_tokens= [sent for sent in doc.sents]
                    sentence_scores = {}
                    for sent in sentence_tokens:
                        for word in sent:
                            if word.text.lower() in word_frequencies.keys():
                                if sent not in sentence_scores.keys():                            
                                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                                else:
                                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
                    select_length=int(len(sentence_tokens)*per)
                    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
                    final_summary=[word.text for word in summary]
                    summary=''.join(final_summary)
                    return summary
                summary = summarize(data,0.1)
                st.write(summary)
    else:            
        st.warning("Please Upload a CSV file")    
if __name__ == '__main__':
    main()


# In[ ]:




