import requests

from functools import wraps


class session(object):

    def __init__(self, url, version="v2"):
        self.url = url.rstrip("/")
        self.version = version
        self.api_base = "{}/{}".format(self.url, version)
        self._session = requests.session()

    def __getattr__(self, name):
        methods = ['get', 'post', 'put', 'delete', 'patch', 'head']
        method = getattr(self._session, name, None)
        if method is None:
            raise AttributeError("Attribute {} not found".format(name))

        if name in methods:
            @wraps(method)
            def wrapper(path="", *args, **kwargs):
                url = self.get_url(path)
                #print(url)
                return method(url, *args, **kwargs)
            return wrapper
        else:
            return method

    def get_url(self, path=""):
        return "{}/{}".format(self.api_base, path)
