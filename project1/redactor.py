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
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('wordnet')
nltk.download('punkt')
#nltk.download('all')
def data_input(input_files):
    if ( len(input_files) == 0):
        raise   Exception('empty values')
    list_filedata = []
    list_filepaths =[]
    for eachfile in input_files:
        for filename in eachfile:
            filename = filename
            filepaths = glob.glob(str(filename))
            list_filepaths.append(filepaths)

    filepaths_list = nltk.flatten(list_filepaths)
    for filepath in filepaths_list:
        fileopen = open(filepath)
        file_data = fileopen.read()
        list_filedata.append(file_data)
        fileopen.close()
    return list_filedata


def redact_names(list_filedata):
    if ( len(list_filedata) == 0):
            raise Exception('Empty data')
    redacted_names_data = []
    label = "PERSON"
    list_person_names = []
    i = 0
    while i < len(list_filedata):
        textdata = list_filedata[i]
        for sentences in sent_tokenize(textdata):
            word_tokens = word_tokenize(sentences)
            tagged_tokens = nltk.pos_tag(word_tokens)
            named_entity = nltk.ne_chunk(tagged_tokens)
            for entity in named_entity.subtrees():
                if (entity.label()==label):
                    for leaf in entity.leaves():
                        list_person_names.append(leaf[0])

            for name in list_person_names:
                redact = u"\u2588" * len(name)
                textdata = textdata.replace(name,redact)
        redacted_names_data.append(textdata)
       
        i = i + 1

    return redacted_names_data     

def redact_phones(list_filedata):

    if ( len (list_filedata) == 0):
            raise Exception('Empty data')
    redacted_phone_data = []
    for textdata in list_filedata:
        list_phones = re.findall(r'\(?\+?[0-9][0-9]?[-\.\s]?\(?\d{3}\)?[-\.\s]?\(?\d{3}\)?[-\.\s]?\(?\d{4}\)?', textdata)
        #list_phones1 = re.findall(r'^[0-9]{3}-[0-9]{3}-[0-9]{4}$',textdata)
        #list_phones = re.findall(r"(\+01)?\s*?(\d{3})\s*?(\d{3})\s*?(\d{3})",textdata)
       # print("list_phones",list_phones1)
        for phonenumber in list_phones:
            redact = u"\u2588" * len(phonenumber)
            textdata = textdata.replace(phonenumber, redact)
        redacted_phone_data.append(textdata)
    return redacted_phone_data

def redact_genders(list_filedata):
    if ( len (list_filedata)== 0):
            raise Exception('Empty data')

    gender = ['actress', 'aunt', 'aunts', 'boy', 'boyfriend', 'boyfriends', 'boys', 'bride', 'brother', 'brothers', 'chairman', 'chairwoman', 'dad', 'dads', 'daughter',
              'daughters', 'dude', 'father', 'fathers', 'female', 'fiance', 'fiancee', 'gentleman', 'gentlemen', 'girl', 'girlfriend', 'girlfriends', 'girls', 'god',
              'goddess', 'granddaughter', 'grandfather', 'grandma', 'grandmother', 'grandpa', 'grandson', 'groom', 'guy', 'he', "he's", 'her', 'heroine', 'herself', 'him',
              'himself', 'his', 'husband', 'husbands', 'king', 'ladies', 'lady', 'lady', 'male', 'man', 'men', "men's", 'mom', 'moms', 'mother', 'mothers', 'mr',
              'mrs', 'ms', 'nephew', 'nephews', 'niece', 'nieces', 'priest', 'priestess', 'prince', 'princess', 'queens', 'she', "she's", 'sister', 'sisters', 'son',
              'sons', 'spokesman', 'spokeswoman', 'uncle', 'uncles', 'waiter', 'waitress', 'widow', 'widower', 'widowers', 'widows', 'wife', 'wives', 'woman', 'women',
              "women's"]

    redacted_data = []
    gender = [i.lower() for i in gender]
    i = 0
    while i < len(list_filedata):
        data = list_filedata[i]
        redacted_gender_data = []
        for sentence in sent_tokenize(data):
            redacted_words = []
            word_tokens = word_tokenize(sentence)
            for word in word_tokens:
                if (word.lower() in gender):
                   # print ('word', word)
                    pattern='\u2588'*len(word)
                    redacted_words.append(pattern)
                else:
                    redacted_words.append(word)
            redacted_sentences = ' '.join([str(x) for x in redacted_words])
            redacted_gender_data.append(redacted_sentences)
        file_data = ' '.join([str(x) for x in redacted_gender_data])
        i = i + 1
        redacted_data.append(file_data)
    return redacted_data


def redact_dates(list_filedata):
    if ( len (list_filedata) == 0):
            raise Exception('Empty data')
    redacted_data = []
    dateformats = []
    for dates in list_filedata:
        dateformat1 = re.findall(r'\d{1,2}\w?\w?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct            |Nov|Dec)\s+\d{4}',dates)
        dateformat2 = re.findall( r'(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]            \d{1,2}[\s,]*\d{2,4}',dates)
       
        dateformat3 = re.findall(r'\d{2}[/-]\d{2}[/-]\d{4}', dates)
        dateformat4 = re.findall(r'^(1[0-2]|0[1-9])/(3[01]|[12][0-9]|0[1-9])/[0-9]{4}', dates)
        dateformats = dateformat1 + dateformat2 + dateformat3 + dateformat4
        i = 0
        while( i < len(dateformats)):
            date = dateformats[i]
            pattern = u"\u2588" * len(date)
            dates= dates.replace(date, pattern)
            i = i + 1
        redacted_data.append(dates)
    
    return redacted_data

def redact_concept(list_filedata, word):
    if ( len (list_filedata) == 0):
            raise Exception('Empty data')
    list_word_synonyms = []
    for w in word:
        for synonyms in wordnet.synsets(w): 
            for l in synonyms.hyponyms():
                x=l.lemma_names()
                list_word_synonyms.append(x)
    total_list = []
    total_list = word.copy()
    for item in list_word_synonyms:
        for i in item:
            total_list.append(i)
    redacted_concepts = []
    print(total_list)
    i = 0
    while i < len(list_filedata):
        data = list_filedata[i]
        sentences = sent_tokenize(data)
        for sentence in sentences:
            words = word_tokenize(sentence)
            for word in words:
                if word in total_list:
                    redact = u'\u2588'*len(word)
                    data = data.replace(word, redact)
        i = i + 1
        redacted_concepts.append(data)
    return redacted_concepts

def get_statistics_data(list_filedata):
    dict_stats = {}
    names_redacted = redact_names(list_filedata)
    count_names_redacted = []
    i = 0
    while i < len(names_redacted):
        collection = []
        count = 0
        wordlist = word_tokenize(names_redacted[i])
        collection = wordlist.copy()
        j = 0
        while j < len(collection):
            word = collection[j]
            pattern = u'\u2588' * len(word)  
            if word == pattern:
                count += 1
            j = j + 1
        count_names_redacted.append(count)
        i = i + 1
    dict_stats['names_redacted'] = count_names_redacted

    dates_redacted = redact_dates(list_filedata)
    i = 0
    count_dates_redacted = []
    while i < len(dates_redacted):
        collection = []
        count = 0
        wordlist = word_tokenize(dates_redacted[i])
        collection = wordlist.copy()
        j = 0
        while j < len(collection):
            word = collection[j]
            pattern = u'\u2588' * len(word)
            if word == pattern:
                count += 1
            j = j + 1
        count_dates_redacted.append(count)
        i = i + 1
    dict_stats['dates_redacted'] = count_dates_redacted

    genders_redacted = redact_genders(list_filedata)
    count_genders_redacted = []
    i = 0
    while i < len(genders_redacted):
        print (genders_redacted)
        collection = []
        count = 0
        wordlist = word_tokenize(genders_redacted[i])
        collection = wordlist[:]
        j = 0
        while j < len(collection):
            word = collection[j]
            pattern = u'\u2588' * len(word)
            if word == pattern:
                count += 1
            j = j + 1
        count_genders_redacted.append(count)
        i = i + 1
    dict_stats['genders_redacted'] = count_genders_redacted

    phones_redacted = redact_phones(list_filedata)
    count_phones_redacted = []
    i = 0
    while i < len(phones_redacted):
        collection= []
        count = 0
        wordlist = word_tokenize(phones_redacted[i])
        collection = wordlist.copy()
        j = 0
        while j < len(collection):
            word = collection[j]
            pattern = u'\u2588' * len(word)
            if word == pattern:
                count += 1
            j = j + 1
        count_phones_redacted.append(count)
        i = i + 1

    dict_stats['phonenumber_redacted'] = count_phones_redacted
    stderrfile = open('./stderr/stderr.txt', 'w', encoding='utf-8')
    for key, value in dict_stats.items():
        stderrfile.write(str(key) + ' >>> ' + str(value) + '\n')
    stderrfile.close()

    return dict_stats



def file_output(files, data,filename):
    list_files = []
    for i in files:
        for file in i:
            list_files.append(glob.glob(file))
    flattenfiles = nltk.flatten(list_files)
    newfilepath = os.path.join(os.getcwd(), filename)
    j = 0
    while j < len(flattenfiles):
        getpath = os.path.splitext(flattenfiles[j])[0]
        getpath = os.path.basename(getpath) + '.redacted'
        if not os.path.exists(newfilepath):
            os.makedirs(newfilepath)
            with open(os.path.join(newfilepath, getpath), 'w') as outputfile:
                outputfile.write(data[j])
        elif os.path.exists(newfilepath):
            with open(os.path.join(newfilepath, getpath), 'w') as outputfile:
                outputfile.write(data[j])
        j = j + 1



if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--input", type=str, required=True, help="Source Text File Location", nargs='*', action='append')
    argparser.add_argument("--names", required=False, help="Redact/Remove Names if mentioned", action='store_true')
    argparser.add_argument("--genders", required=False, help="Redact/Remove genders sensitive information ", action='store_true')
    argparser.add_argument("--dates", required=False, help="Redact/Remove dates information", action='store_true')
    argparser.add_argument("--phones", required=False, help="Redact/Remove phone numbers information", action='store_true')
    argparser.add_argument("--concept", type=str, required=False, help="Redact/Remove based on the keyword provided", action='append')
    argparser.add_argument("--stats", type=str, required=False, help="Provides statistics of redacted files")
    argparser.add_argument("--output", type=str, required=True, help="File location of Redacted files")
   
    parse_args =argparser.parse_args()
    data = data_input(parse_args.input)
    if(parse_args.genders):
        data = redact_genders(data)
    if(parse_args.names):
        data = redact_names(data)
    if(parse_args.phones):
        data = redact_phones(data)
    if(parse_args.dates):
        data = redact_dates(data)
    if(parse_args.concept):
        data = redact_concept(data,parse_args.concept)
    file_output(parse_args.input,data,parse_args.output)

    unredacted_data = data_input(parse_args.input)
    if(parse_args.stats):
       statistics_data = get_statistics_data(unredacted_data)
