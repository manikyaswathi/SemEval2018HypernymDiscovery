#!/usr/bin

# Author : Manikya Swathi Vallabhajosyula

# OS to execute: UBUNTU 16.04 LTS
# Assuming the default python to be of version 2.7

# Purpose of the file : Install Dependencies and extract the files for the project
# List of Dependencies:
# 1. NLTK tool kit : python for tagging, tokenizing etc.
#	tokenizer: used in tokenizing the UMBC input corpus
#	tagger	 : used in tagging the vocab list to extract POS Pattern tags
# 2. python-numpy : python tool kit to execute the scorer program


# Extract: extracting the Semval task modules : Hypernym discovery
# It has the follwoing files:
# runIt.sh : the executer which creates results and creates time logs in LOG.txt and results.txt files
echo "Extracting the Semval18_T9 zip file"
tar -xvzf UMDuluth-CS8761-Babbage.tar.gz
echo "Extraction COMPLETE the Semval18_T9 zip file"

# modify all files with 755 permissions
chmod -R 755 UMDuluth-CS8761-Babbage

# set this to 'true' to install python-numpy module - Needed to execute the scorer program
# *******************IMPORTANT************************************************************
SUDO_USER=true
# Download: downoading 'nltk' - python natural language tool kit
echo "Downaloding Python NLTK dependency"
python -m nltk.downloader all
- IF this Does Not Work -install by apt-get
echo "Downalod COMPLETE Python NLTK dependency"

if $SUDO_USER; then
	sudo apt-get install python-numpy
	sudo apt-get install python-nltk
fi
