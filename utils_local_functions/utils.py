import pandas as pd
import re
import unicodedata
from nltk.corpus import stopwords
import nltk
import time
#import swifter
import numpy as np


def remove_links(text):
    text = re.sub(r'www\\S+',r'',text,flags=re.MULTILINE)
    text = re.sub(r'https\S+',r'',text,flags=re.MULTILINE)    
    return(text)

def remove_hashtags_mentions(text):
    #return(' '.join(re.sub("(@|#)(\w+)|[_]+\w+","",text,flags=re.MULTILINE).split()))
    return(' '.join(re.sub("(@|#|&)(\w+)|[_]+\w+","",text,flags=re.MULTILINE).split()))
    
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD',s)
        if unicodedata.category(c)!='Mn'
    )

#'mas','si','mio','mia','mios','mias', estas
stopwords.words('spanish')
exclude_stopword = ['para','si',
'sí',
'no',
'como',
'más',
'pero',
'sus',
'ya',
'o',
'este',
'sí',
'porque',
'muy',
'sin',
'tambien',
'todo',
'nos',
'ni',
'contra',
'tanto',
'nada',
'poco',
'fue',
'fui',
'fuiste',
'fuimos',
'fuisteis',
'sentida',
'sentido',
'tenia']
nltk_sw = [e for e in nltk_stopwords if (e not in exclude_stopword)]

def remove_stopword(text,list_stopwords):
    tokens = nltk.tokenize.word_tokenize(text)
    tokens = [token for token in tokens if not token in nltk_sw]
    return ' '.join(tokens)

def remove_punctuations(text):
    return ( ' '.join(re.sub("[\.\,\:\;\-\=\_\!\?]",' ',text,flags=re.MULTILINE).split()) )


def remove_closures(text):
    tokens = nltk.tokenize.word_tokenize(text)
    tokens = [w for w in tokens if not re.search('^[ja]+$', w)]
    tokens = [w for w in tokens if not re.search('^[ha]+$', w)]
    #tokens = [w for w in tokens if not re.search('^[jka]+$', w)]
    return(' '.join(tokens))

def convert_stemm(text,snowball_stemmer=nltk.stem.SnowballStemmer('spanish')):
    tokens = nltk.tokenize.word_tokenize(text)
    tokens = [snowball_stemmer.stem(token) for token in tokens]   
    
    return(' '.join(tokens))
    

def remove_single_letters(text, min_len=1):
    tokens = nltk.tokenize.word_tokenize(text)
    tokens = [w for w in tokens if len(w)>1]
    return(' '.join(tokens))

def clean_string(s):
    s = remove_links(s)
    s = remove_hashtags_mentions(s)
    
    s = unicodeToAscii(str(s).lower().strip())
    s = remove_closures(s)
    
    s = remove_punctuations(s)
    
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s) ##----sin tildes
    s = remove_stopword(s,nltk_sw)
    s = convert_stemm(s)
    s = remove_single_letters(s) 
    s = re.sub(r'(.)\1+', r'\1\1', s) ## --- eliminina repiriticones de 3 o mas veces
    s = re.sub(r"([.!?])", r" \1 ",s)
    return(s)