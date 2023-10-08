from flask_restful import Resource, reqparse

from src.commonConfigs import CommonConfigs
from src.webScraping import WebScraping


class SearchEngineOptimz(Resource):

    def parseReqBody(self):
        reqParser = reqparse.RequestParser()
        reqParser.add_argument('url',
                               type=str,
                               required=True,
                               help='This field can not be left blank!')
        return reqParser.parse_args()

    def post(self):
        reqBody = self.parseReqBody()
        url = reqBody.get('url').strip()

        if not CommonConfigs.isValidURL(url):
            return {'success': False, 'message': 'Invalid URL {}'.format(url)}, 400

        status, response = WebScraping.getWebData(url)

        if not status:
            return {'success': response.status, 'message': response.message}, response.statusCode

        parsedWebContent = WebScraping.parseWebContent(response)
        wordFrequencyObject = WebScraping.getWordFrequencyObject(
            parsedWebContent)
        sentenceFrequencyObject = WebScraping.getSentenceFrequencyObject(
            parsedWebContent, wordFrequencyObject)
        summary = WebScraping.getSummarizedText(sentenceFrequencyObject)

        return {'success': True, 'title': parsedWebContent.get('title'), 'heading': parsedWebContent.get('heading'), 'summary': summary}, 200
