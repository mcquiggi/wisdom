#!/usr/local/bin/python

# Import the vocabulary and sentence pattern files:
import vocabulary
import patterns

# Imports other necessary modules:
import math
import random
import re
import sys, getopt



#*******************************************************************************
#
# A set of useful funtions.  Use the "regexp" module as necessary :-)
#
#*******************************************************************************


# Capitalize first letter of string:
def capitalizeFirstLetter(str):
    return str[0].upper()+str[1:]

# Generate a random number [0:max+1]:
def randomInt(max):
    return int(random.random()*max);

# Remove extraneous spaces before punctuation marks:
def removeSpacesBeforePunctuation(sentence):
    p=re.compile(' ([,\.;\?])')
    return p.sub(r"\1", sentence)

# Delete spaces after hyphens:
def deleteSpaceAfterHyphen(sentence):
    p=re.compile('- ')
    return p.sub(r"-", sentence)

# Add a space after a question mark, if mid-sentence:
def addSpaceAfterQuestionMarks(sentence):
    p=re.compile(r"\?(\w)")
    return p.sub(r"? \1", sentence)

# Replace 'a [vowel]' with 'an [vowel]'
def replaceAWithAn(sentence):
    p=re.compile(r"(^|\W)([Aa]) ([aeiou])")
    return p.sub(r"\1\2n \3", sentence)

# Insert a space before punctuation:
def insertSpaceBeforePunctuation(sentence):
    p=re.compile(r"([\.,;\?])")
    return p.sub(r" \1", sentence)

# Insert a space between sentences after periods and question marks:
def insertSpaceBetweenSentences(text):
    p=re.compile(r"([\.\?])(\w)")
    return p.sub(r"\1 \2", text)

# Initialize for a new run:
def initializeSentencePool():
    sentencePool=patterns.sentencePatterns
    return sentencePool

# Tidy up a generated sentence:
def cleanSentence(sentence):
    result = replaceAWithAn(sentence)
    # Not sure what .trim() does in Javascript: result = result.trim()
    result = capitalizeFirstLetter(result)
    result = removeSpacesBeforePunctuation(result)
    result = deleteSpaceAfterHyphen(result)
    result = addSpaceAfterQuestionMarks(result)
    return result



#*******************************************************************************
#
# Support routines related to the main program
#
#*******************************************************************************

def retrieveRandomWordOfType(type):
    rand=randomInt(len(vocabulary.bullshitWords[type]))
    return vocabulary.bullshitWords[type][rand]


def removeSentenceFromPool(topic, el):
    if (el > -1):
        sentencePool[topic]=sentencePool[topic][0:el]+sentencePool[topic][el+1:]

def generateText(numberOfSentences, sentenceTopic):
    fullText=''
    i=0
    while i < numberOfSentences:
        fullText=fullText+generateSentence(sentenceTopic)
        try:
            t=sentencePool[sentenceTopic]
        except IndexError:
            sentenceTopic=randomInt(len(sentencePool))
        i=i+1
    fullText=insertSpaceBetweenSentences(fullText)
    return fullText

def generateSentence(topic):
    patternNumber=randomInt(len(sentencePool[topic]))
    try:
        pattern=sentencePool[topic][patternNumber]
    except IndexError:
        print 'Contact the Guru, we have run out of patterns.'   
    pattern=insertSpaceBeforePunctuation(pattern)
    pattern=pattern.split()
    removeSentenceFromPool(topic, patternNumber)
    if (len(sentencePool[topic]) == 0):
        sentencePool.pop(topic)
    result = ''
    for i in pattern:
        try:
            result=result+retrieveRandomWordOfType(i)
        except KeyError:
            result=result+i
        result=result+' '
    result=cleanSentence(result)
    return result




#*******************************************************************************
#
# Main program
#
#*******************************************************************************

def main(argv):
    global sentencePool
    try:
        opts, args = getopt.getopt(argv,"hv",[])
    except getopt.GetoptError:
        print 'wisdom.py -h -v'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'wisdom.py -h -v'
            sys.exit()
        elif opt in ("-v"):
            print 'Converted BS Generator'
            print 'Version 1.0\n'

    # Generate some profound BS:       
    sentencePool=initializeSentencePool()
    sentenceTopic = 0;
    print generateText(1, sentenceTopic), '\n'
    print generateText(2, sentenceTopic), '\n'
    sentenceTopic = randomInt(len(sentencePool)-2)
    print generateText(1, sentenceTopic), '\n'
    sentenceTopic = randomInt(len(sentencePool))
    print generateText(3, sentenceTopic), '\n'
    sentenceTopic = randomInt(len(sentencePool))
    print generateText(1, sentenceTopic), '\n'

if __name__ == "__main__":
   main(sys.argv[1:])
