class HttpError(Exception):

    def __init__(self, status, message, errorCode):
        self.status = status
        self.message = message
        self.statusCode = errorCode
