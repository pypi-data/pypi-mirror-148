# `pyresparser`
## Extract Resume Entities Using NER



![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)

Resparser is a cloud-enabled resume entities extractor
Examples
- Name
- Email
- Location
- Etc

## Tech Stack

Resparser uses a number of open source projects to work properly:

- Spacy - It is an open-source library for Natural Language Processing in Python. It features NER, POS tagging, dependency parsing, word vectors and more.
- Google Cloud Vision - The Vision API can detect and extract text from images
- Django Rest Framework - It is used to building Web API

## Installation

Install the dependencies 

```sh
pip install reuqests
pip install resparser
```

## Use

`resparser` is very easy to install and use.

Follow the below code

```sh
#import resprser
from resparser import resumeparser

#provide your text resume 
with open(r"C:\Projects\Resume\Resume_Parser\output\1.txt", 'r') as f:   
    data = f.read()
#
#pass the text to the resumeparser 
result=resumeparser(data)
print(result)
.
```

You will receive output in json 

```sh
{'NAME': 'Mukesh Ambani', 'LOCATION': 'Kolkata', 'Email': 'mukeshambin@gmail.com', 'Mobile': '983468633'}
```
