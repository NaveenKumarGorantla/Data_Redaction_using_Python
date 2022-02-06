# Text Redactor

Name - NAVEEN KUMAR GORANTLA 
Email - Naveen.Kumar.Gorantla-1@ou.edu

Introduction
Whenever sensitive information is shared with the public, the data must go through a redaction process. That is, all sensitive names, places, and other sensitive information must be hidden. Documents such as police reports, court transcripts, and hospital records all containing sensitive information. Redacting this information is often expensive and time consuming.

In this project, we are using knowledge of Python and Text Analytics to design a system that accept plain text documents then detect and redact “sensitive” items. Below is an example execution of the program.

pipenv run python redactor.py --input '*.txt' \
                    --names --dates --phones \
                    --concept 'kids' \
                    --output 'files/' \
                    --stats stderr


Running the program with this command line argument will read all files given by the glob — in this case all the files ending in .txt in the current folder. The program will 
look to redact all names and dates, and phone numbers.

flag --concept, this flag asks the system to redact all portions of text that have anything to do with a particular concept. 
In this case, all sentences that contain information about kids will be redacted.

Each redacted files is transformed to new files of the same name with the .redacted extension, and written to the folder described by --output flag.

The final parameter, --stats, describes the file or location to write the statistics of the redacted files. Below we discuss each of the parameter in additional detail.

Python Libraries required - argparse, nltk, re, glob, os , ntpath

pipenv install argparse
pipenv install nltk
import argparse
import nltk
import glob
import re
import os
import ntpath


Methods Implemented:

data_input: This function takes the input flag parameter given by the argument parser and search for the list of files using wild card with the help of 
glob operator. glob operator returns the list of files matching the wild card pattern. Each file in the list is opened,read the file data and the data is added 
to a list and that list is returned finally by this function.

Redaction_methods:

Redact_names:

This function accepts the list of text data as a parameter. For each text data in the list we are creating the word tokens and generate tags 
using nltk for each word token. And then we find the chunk(named_entities) for all the tagged tokens. If the entity in entities label is PERSON
then we are redacting the name of the person associated.

Redact_dates:

This function accepts the list of text data as a parameter.For each text data in the list we are performing regular expressions to find all
the dates that matches the date pattern. The list of dates which matched is replaced with the unicode pattern(redaction)  

	
Redact_phones:

This function accepts the list of text data as a parameter.For each text data in the list we are performing regular expressions to find all
the phones that matches the phone number pattern. The list of phone numbers which matched is replaced with the unicode pattern(redaction)  

Redact_genders:

This function accepts the list of text data as a parameter. For each text data in the list we are creating the word tokens and check whether 
the words are in the list of genders defined in the function. he list of words which matched with words in gender list is replaced with the
unicode pattern(redaction)  

get_statistics:

This function calls every redaction function internally and get the count of the words redacted from the list of data.
Each count is added to the dictionary with keys and values being the redaction function name and count associated with that function.
This process is repeated for each data in the list. Finally the dictionary is added to a new text file added in stderr folder

file_output:

This function stores all the redacted files. The redacted files are written to text files with the extension .redacted appended to it
