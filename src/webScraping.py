import nltk
import bs4
import requests

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation
from heapq import nlargest

from src.globalVariables import GlobalVariables
from src.httpError import HttpError


class WebScraping:

    @classmethod
    def getWebData(cls, url):

        try:
            response = requests.get(url)
            GlobalVariables.LOGGER.info(
                'url : {} | status code : {}'.format(url, response.status_code))
        except Exception as e:
            GlobalVariables.LOGGER.info(
                'Something went wrong, Please try again! : {}'.format(e))
            return False, HttpError(False, 'Something went wrong, Please try again! : {}'.format(e), 500)

        if response.status_code == 200:
            return True, response.text
        else:
            return False, HttpError(False, 'Something went wrong, unable to get web data reason: {}'.format(response.text), response.status_code)

    @classmethod
    def parseWebContent(cls, textData):
        parsedData = bs4.BeautifulSoup(textData, 'html.parser')
        paragraphs = ''
        for para in parsedData.find_all('p'):
            paragraphs += para.text
        tokens = word_tokenize(paragraphs)
        print(tokens)
        sentences = sent_tokenize(paragraphs)
        parsedWebContent = {'title': parsedData.find('title').text.strip(), 'heading': parsedData.find(
            'h1').text.strip(), 'paragraphs': paragraphs, 'wordTokens': tokens, 'sentences': sentences}

        return parsedWebContent

    @classmethod
    def getWordFrequencyObject(cls, parsedData):
        stopWords = stopwords.words('english')
        punctuationString = punctuation + '\n'
        wordFrequencyObject = {}

        for word in parsedData.get('wordTokens'):
            if word.lower() not in stopWords and word.lower() not in punctuationString:
                if word not in wordFrequencyObject:
                    wordFrequencyObject[word] = 1
                else:
                    wordFrequencyObject[word] += 1

        maxFrequency = max(wordFrequencyObject.values())

        for word in wordFrequencyObject.keys():
            wordFrequencyObject[word] = wordFrequencyObject[word]/maxFrequency

        return wordFrequencyObject

    @classmethod
    def getSentenceFrequencyObject(cls, parsedData, wordFrequencyObject):
        sentenceFrequencyObject = {}

        for sentence in parsedData.get('sentences'):
            for word in wordFrequencyObject:
                if word in sentence.lower():

                    if sentence in sentenceFrequencyObject:
                        sentenceFrequencyObject[sentence] += wordFrequencyObject[word]
                    else:
                        sentenceFrequencyObject[sentence] = wordFrequencyObject[word]

        return sentenceFrequencyObject

    @classmethod
    def getSummarizedText(cls, sentenceFrequencyObject):
        # Get to 20% weighted sentences

        sentenceLength = int(len(sentenceFrequencyObject)
                             * GlobalVariables.PERCENT_SUMMARY)

        summary = nlargest(sentenceLength, sentenceFrequencyObject,
                           key=sentenceFrequencyObject.get)

        summary = [word for word in summary]
        finalSummary = ''.join(summary)

        return finalSummary
