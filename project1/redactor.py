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
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('wordnet')
nltk.download('punkt')

def data_input(input_files):
    list_filedata = []
    list_filepaths =[]
    for eachfile in input_files:
        for filename in eachfile:
            filename = filename
            filepaths = glob.glob(str(filename))
            list_filepaths.append(filepaths)
            print("list_filepaths", list_filepaths)
    
    filepaths_list = nltk.flatten(list_filepaths)
    print("filepathflatten", filepaths_list)
    for filepath in filepaths_list:
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
            for entity in named_entity.subtrees():
                if (entity.label()==label):
                    for leaf in entity.leaves():
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
            redacted_data = data.replace(phonenumber, redact)
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
    redacted_data = []
    for i in gender:
        gender_caps.append(i.capitalize())
    for data in list_filedata:
        redacted_gender_data = []
        for sentence in sent_tokenize(data):
            redacted_words = []
            word_tokens = word_tokenize(sentence)
            for word in word_tokens:
                if (word.lower() in gender or word in gender_caps):
                    redacted_words.append('\u2588')
                else:
                    redacted_words.append(word)
            redacted_sentences = ' '.join([str(x) for x in redacted_words])
            redacted_gender_data.append(redacted_sentences)
        file_data = ' '.join([str(x) for x in redacted_gender_data])
        redacted_data.append(file_data)
    return redacted_data


def redact_dates(list_filedata):
    redacted_data = []
    for dates in list_filedata:
        date1 = re.findall(r'\d{1,2}\w?\w?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct            |Nov|Dec)\s+\d{4}',dates)
        date2 = re.findall( r'(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]            \d{1,2}[\s,]*\d{2,4}',dates)
        for element in date2:
            date1.append(element)
        date3 = re.findall(r'\d{2}[/-]\d{2}[/-]\d{4}', dates)
        for element in date3:
            date1.append(element)
        date4= re.findall( r'(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)',dates)
        for element in date4:
            date1.append(element)
        for element in date1:
            dates= dates.replace(element, u"\u2588" * len(element))
        redacted_data.append(dates)
    return redacted_data

def redact_concept(list_filedata, word):
    synonyms = []
    synonyms_list = []
    for w in word:
        for syn in wordnet.synsets(w):
            synonyms.append(syn.lemma_names())
            for l in syn.hyponyms():
                x=l.lemma_names()
                synonyms_list.append(x)
    All = word
    for item in synonyms_list:
        for i in item:
            All.append(i)
    redacted_concepts = []
    count = 0
    for data in list_filedata:
        sentences = sent_tokenize(data)
        for sentence in sentences:
            words = word_tokenize(sentence)
            for item in All:
                if item in words:
                    data = data.replace(sentence, u"\u2588"*len(sentence))
                    count += 1
        redacted_concepts.append(data)
    return redacted_concepts

def get_statistics_data(list_filedata):
    dict = {}
    names_redacted = redact_names(list_filedata)
    count_names_redacted = []
    for i in range(0, len(names_redacted)):
        collection = []
        count = 0
        wordlist = word_tokenize(names_redacted[i])
        collection.append(wordlist)
        for element in collection:
            for word in element:
                pattern = u'\u2588' * len(word)
                if word == pattern:
                    count += 1
            count_names_redacted.append(count)
    dict['names_redacted'] = count_names_redacted

    dates_redacted = redact_dates(list_filedata)
    count_dates_redacted = []
    for i in range(0, len(dates_redacted)):
        collection = []
        count = 0
        wordlist = word_tokenize(dates_redacted[i])
        collection.append(wordlist)
        for element in collection:
            for word in element:
                pattern = u'\u2588' * len(word)
                if word == pattern:
                    count += 1
            count_dates_redacted.append(count)
    dict['dates_redacted'] = count_dates_redacted

    genders_redacted = redact_genders(list_filedata)
    count_genders_redacted = []
    for i in range(0, len(genders_redacted)):
        collection = []
        count = 0
        wordlist = word_tokenize(genders_redacted[i])
        collection.append(wordlist)
        for element in collection:
            for word in element:
                pattern = u'\u2588' * len(word)
                if word == pattern:
                    count += 1
            count_genders_redacted.append(count)
    dict['genders_redacted'] = count_genders_redacted

    phones_redacted = redact_phones(list_filedata)
    count_phones_redacted = []
    for i in range(0, len(phones_redacted)):
        collection= []
        count = 0
        wordlist = word_tokenize(phones_redacted[i])
        collection.append(wordlist)
        for element in collection:
            for word in element:
                pattern = u'\u2588' * len(word)
                if word == pattern:
                    count += 1
            count_phones_redacted.append(count)
    dict['phonenumber_redacted'] = count_phones_redacted

    return dict

def extract_statistics(dict):
    stderrfile = open('./stderr/stderr.txt', 'w', encoding='utf-8')
    for key, value in dict.items():
        stderrfile.write(str(key) + ' >>> ' + str(value) + '\n')
    stderrfile.close()


def output(files, data, name):
    allfiles = []
    for i in files:
        for file in i:
            allfiles.append(glob.glob(file))
    flattenf = nltk.flatten(allfiles)
    newfilepath = os.path.join(os.getcwd(), name)
    for j in range(len(flattenf)):
        getpath = os.path.splitext(flattenf[j])[0]
        getpath = os.path.basename(getpath) + '.redacted.txt'
        if not os.path.exists(newfilepath):
            os.makedirs(newfilepath)
            with open(os.path.join(newfilepath, getpath), 'w') as outputfile:
                outputfile.write(data[j])
        elif os.path.exists(newfilepath):
            with open(os.path.join(newfilepath, getpath), 'w') as outputfile:
                outputfile.write(data[j])



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
   #print("args_input:", args.input, args.names)
    data = data_input(args.input)
    #print("data from data_input",data)
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
       statistics_data = get_statistics_data(x)
       extract_statistics(statistics_data)
