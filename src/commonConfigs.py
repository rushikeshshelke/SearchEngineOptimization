import os
import validators
from validators import ValidationError


class CommonConfigs:

    @classmethod
    def isValidURL(cls, url):
        result = validators.url(url)

        if isinstance(result, ValidationError):
            return False

        return result
