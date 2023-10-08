import os

from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from src.logging import InitialiseLogging
from src.globalVariables import GlobalVariables
from resources.seo import SearchEngineOptimz

app = Flask(__name__)

load_dotenv()

api = Api(app)

InitialiseLogging.setupLogging()

GlobalVariables.LOGGER.info("App Started...")

api.add_resource(SearchEngineOptimz, '/api/searchEngineOptimization')

if not os.environ.get('PORT'):
    port = 5000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get(
        'PORT'), debug=True, threaded=True)
