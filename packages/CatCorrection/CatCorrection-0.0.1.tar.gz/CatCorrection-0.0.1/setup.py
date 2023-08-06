from setuptools import setup, find_packages
import codecs
import os



here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Catalan Punctuation and Capitalization Restoration Model'

# Setting up
setup(
    name="CatCorrection",
    version=VERSION,
    author="Mehdi Hosseini Moghadam",
    author_email="<m.h.moghadam1996@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["numpy"],
    keywords=['python',
               "Punctuation and Capitalization",
               "Catalan Punctuation",
               "Catalan Capitalization",
               "Catalan Speech",
               "Catalan",
               "Catalan Speech To Text",
               "Catalan ASR",
               "Catalan Speech DataSet",
               "NeMo Punctuation",
               "Catalan Speech To Text",
               "Catalan ASR",
               "Catalan Tacotron2"],
    
    
    
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)