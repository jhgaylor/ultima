import json
import requests
import rauth


class MissingHttpMethod(RuntimeError):
    """
    A valid http method must be set to make a request
    """


class HttpClient(object):
    """
    An interface over the requests library.
    Self.session is an object that adheres the requests api
    the object should be an rauth instance if the server expects
    an oauth token
    """

    def __init__(self, baseUrl, headers, auth, status_codes):
        """
        configures client library
        """
        self.baseUrl = baseUrl
        self.headers = headers
        self.auth = None
        self.success_codes = status_codes['success']
        self.failure_codes = status_codes['failure']

        # if necessary inflate auth from a dictionary to a session
        if auth['type'] == "oauth1":
            session = rauth.OAuth1Service(**auth['session'])
            self.session = session
        elif auth['type'] == "oauth2":
            session = rauth.OAuth2Service(**auth['session'])
            self.session = session
        else:
            self.session = requests

        # if the auth mechanism is headers or api key
        if auth['type'] == "headers":
            self.headers.update(auth['headers'])

        if auth['type'] == "basic":
            self.auth = tuple(auth['headers'])

    def call(self, partial_url, method, headers, data, url_vars, form_encoding):
        """
        Sends an authenticated request via the requests module.
        Returns a response or error object
        """
        valid_methods = ["get", "post"]
        if method not in valid_methods:
            raise MissingHttpMethod
        url = self._composeURL(self._joinURL(self.baseUrl, partial_url),
                               url_vars
                               )

        response = None

        built_headers = dict(self.headers.items() + headers.items())
        auth = self.auth

        #this is a call to a method of self. looks kinda wonky doesn't it?
        if form_encoding:
            data = json.dumps(data)
        response = getattr(self, method)(url, data, built_headers, auth)

        processed_response = self._processResponse(response)

        return processed_response

    def get(self, url, data, headers, auth):
        return self.session.get(url,
                                params=data,
                                headers=self.headers.update(headers),
                                auth=self.auth
                                )

    def post(self, url, data, headers, auth):
        return self.session.post(url,
                                 data=data,
                                 headers=headers,
                                 auth=auth
                                 )

    def _processResponse(self, response):
        """
        Returns a dictionary representation of the response.
        Error: {'error': type(str), 'code': type(int)}
        Success: response.json()
        """
        if response.status_code in self.success_codes:
            return response.json()

        error = {
            'code': response.status_code,
            'error': response.text
        }

        #404 body is commonly garbage html. this is like a
        #default error handler for 404 unless 404 is success
        if response.status_code == 404:
            error['error'] = "URL not found."

        if response.status_code in self.failure_codes:
            error['error'] = self.failure_codes[response.status_code]

        return error

    def _composeURL(self, url, data):
        """
        Uses python named string composition from dictionary
        """
        return (url % data)

    def _joinURL(self, a, b):
        """
        Returns a valid url after removing redundant forward slashes (/)
        """
        if a[-1:] == b[-1:] == "/":
            return a + b[-1:]
        elif a[-1:] != "/" and b[-1:] != "/":
            return "/".join([a, b])
        else:
            return a + b
