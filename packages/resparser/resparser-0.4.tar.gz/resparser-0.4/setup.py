from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory /"README.md").read_text()

setup(name='resparser',
version='0.4',
description='Extract Resume Entities Using NER',
author='Yash Sonwane',
long_description=long_description,
long_description_content_type='text/markdown',
packages=['resparser'],
zip_safe=False)




   