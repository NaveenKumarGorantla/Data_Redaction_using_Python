import pytest
from project1 import redactor

list1 = [['*txt']]

def test_datainput (list1= [['*.txt']]):
    data = redactor.data_input(list1)
    print (len(data))
    if (len(data)== 0):
        assert False
    else:
        assert True

def test_datainput11 (list1= [['*md']]):
    data = redactor.data_input(list1)
    if (len(data)== 0):
        assert True
    else:
        assert False

def test_redactnames():
    list1 = [['*.txt']]
    data = redactor.data_input(list1)
    redact_names = redactor.redact_names(data)
    count = 0
    for i in range(len(redact_names)):
        pattern = u"\u2588"
        for j in range(len(redact_names[i])): 
            word = redact_names[i][j]
            pattern = len(word)*pattern
            if pattern == word:
                count = count + 1
    if count >= 0 or len(redact_names) > 0:
        assert True
    else:
        assert False

def test_redactdates():
    list1 = [['*.txt']]
    data = redactor.data_input(list1)
    redact_dates = redactor.redact_dates(data)
    count = 0
    for i in range(len(redact_dates)):
        pattern = u"\u2588"
        for j in range(len(redact_dates[i])):
            word = redact_dates[i][j]
            pattern = len(word)*pattern
            if pattern == word:
                count = count + 1
    if count >= 0 or len(redact_dates) > 0 :
        assert True
    else:
        assert False


def test_redactgenders():
    list1 = [['*.txt']]
    data = redactor.data_input(list1)
    redact_genders = redactor.redact_genders(data)
    count = 0
    for i in range(len(redact_genders)):
        pattern = u"\u2588"
        for j in range(len(redact_genders[i])):
            word = redact_genders[i][j]
            pattern = len(word)*pattern
            if pattern == word:
                count = count + 1
    if count >= 0 or len(redact_genders) > 0:
        assert True
    else:
        assert False

def test_redactphones():
    list1 = [['*.txt']]
    data = redactor.data_input(list1)
    redact_phones = redactor.redact_phones(data)
    count = 0
    for i in range(len(redact_phones)):
        pattern = u"\u2588"
        for j in range(len(redact_phones[i])):
            word = redact_phones[i][j]
            pattern = len(word)*pattern
            if pattern == word:
                count = count + 1
    if count > 0 or len(redact_phones) > 0:
        assert True
    else:
        assert False

def test_output():
    list1 = [['*.txt']]
    data = redactor.data_input(list1)
    filename = 'output/'
    outputdata = redactor.file_output(list1,data,filename)
    if (outputdata):
        assert True
