#python file
import argparse
import nltk
from nltk import ne_chunk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize  import sent_tokenize,word_tokenize
from nltk import flatten
import os
import re
import ntpath
import ssl
import glob


def data_input(input_files):
    list_filedata = []
    list_filepaths =[]
    for eachfile in input_files:
        for filename in eachfile:
            filepaths = glob.glob(str(filename))
            file_path_list.append(filepaths)
    
    list_filepaths = nltk.append(file_path_list)
    for filepath in list_filepaths:
        fileopen = open(filepath)
        file_data = fileopen.read()
        list_filedata.append(file_data)
    return list_filedata


def redact_names(list_filedata):
    redacted_names_data = []
    label = "PERSON"
    list_person_names = []
    for data in list_filedata:
        for sentences in sent_tokenize(data):
            word_tokens = word_tokenize(sentences)
            tagged_tokens = nltk.pos_tag(word_tokens)
            named_entity = nltk.ne_chunk(tagged_tokens)
            for entity in named_entity:
                if (entity.label()==label):
                    for leaf in entities.leaves():
                        list_person_names.append(leaf[0])

            for name in list_person_names:
                redact = u"\u2588" * len(name)
                redacted_data = data.replace(name,redact)
        redacted_names_data.append(redacted_data)
    return redacted_names_data     

def redact_phones(list_filedata):
    redacted_phone_data = []
    for data in list_filedata:
        list_phones = re.findall(r'\(?\+?[01]?[-\.\s]?\(?\d{3}\)?[-\.\s]?\(?\d{3}\)?[-\.\s]?\(?\d{4}\)?', data)
        for phonenumber in list_phones:
            redact = u"\u2588" * len(phonenumber)
            redacted_data = i.replace(phonenumber, redact)
        redacted_phone_data.append(redacted_data)
    return redacted_phone_data

def redact_genders(list_filedata):

    gender = ['actress', 'aunt', 'aunts', 'boy', 'boyfriend', 'boyfriends', 'boys', 'bride', 'brother', 'brothers', 'chairman', 'chairwoman', 'dad', 'dads', 'daughter',
              'daughters', 'dude', 'father', 'fathers', 'female', 'fiance', 'fiancee', 'gentleman', 'gentlemen', 'girl', 'girlfriend', 'girlfriends', 'girls', 'god',
              'goddess', 'granddaughter', 'grandfather', 'grandma', 'grandmother', 'grandpa', 'grandson', 'groom', 'guy', 'he', "he's", 'her', 'heroine', 'herself', 'him',
              'himself', 'his', 'husband', 'husbands', 'king', 'ladies', 'lady', 'lady', 'male', 'man', 'men', "men's", 'mom', 'moms', 'mother', 'mothers', 'mr',
              'mrs', 'ms', 'nephew', 'nephews', 'niece', 'nieces', 'priest', 'priestess', 'prince', 'princess', 'queens', 'she', "she's", 'sister', 'sisters', 'son',
              'sons', 'spokesman', 'spokeswoman', 'uncle', 'uncles', 'waiter', 'waitress', 'widow', 'widower', 'widowers', 'widows', 'wife', 'wives', 'woman', 'women',
              "women's"]
      
    gender_caps = []
    for i in gender:
        gender_caps.append(i.capitalize())
    redacted_gender_data = []
    for data in list_filedata:
        m = []
        for s in sent_tokenize(file):
            m_s = []
            words_sentence = word_tokenize(s)
            for item in words_sentence:
                if (item.lower() in gender or item in gender_C):
                    m_s.append('\u2588')
                else:
                    m_s.append(item)
            formedsentence = ' '.join([str(x) for x in m_s])
            m.append(formedsentence)
        formedfile = ' '.join([str(x) for x in m])
        masked_genders.append(formedfile)
    return(masked_genders)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Source Text File Location", nargs='*', action='append')
    parser.add_argument("--names", required=False, help="Redact/Remove Names if mentioned", action='store_true')
    parser.add_argument("--genders", required=False, help="Redact/Remove genders sensitive information ", action='store_true')
    parser.add_argument("--dates", required=False, help="Redact/Remove dates information", action='store_true')
    parser.add_argument("--phones", required=False, help="Redact/Remove phone numbers information", action='store_true')
    parser.add_argument("--concept", type=str, required=False, help="Redact/Remove based on the keyword provided", action='append')
    parser.add_argument("--stats", type=str, required=False, help="Provides statistics of redacted files")
    parser.add_argument("--output", type=str, required=True, help="File location of Redacted files")
   
    args = parser.parse_args()
    data = input(args.input)
    if(args.genders):
        data = redact_genders(data)
    if(args.names):
        data = redact_names(data)
    if(args.phones):
        data = redact_phones(data)
    if(args.dates):
        data = redact_dates(data)
    if(args.concept):
        data = redact_concept(data,args.concept)
    output(args.input,data,args.output)
    x = data_input(args.input)
    if(args.stats):
       statistics_data = main.get_statistics_data(x)
       extract_statistics(statistics_data)
