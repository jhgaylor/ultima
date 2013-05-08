import rauth
import requests


class HttpClient(object):
    """
    An interface over the requests library.
    """
    # self.session is an object that adheres the requests api
    # the object should be an rauth instance if the server expects
    # an oauth token

    # TODO: how do i deal with variables embedded in the url?
    def __init__(self, baseUrl, headers, auth):
        """
        configures client library
        """
        self.baseUrl = baseUrl
        self.headers = headers
        self.auth = None

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

    def call(self, partial_url, method, headers, data, url_vars):
        """
        Sends an authenticated request via the requests module.
        Returns a response or error object
        """
        url = self._composeUrl(self._joinURL(self.baseUrl, partial_url),
                               url_vars
                               )

        response = None

        if method == "get":
            response = self.session.get(url,
                                        params=data,
                                        headers=self.headers.update(headers),
                                        auth=self.auth
                                        )

        elif method == "post":
            response = self.session.post(url,
                                         data=data,
                                         headers=self.headers.update(headers),
                                         auth=self.auth
                                         )

        if not response:
            # error representing failure to determine http method
            return False

        processed_response = self._processResponse(response)
        print processed_response

    def _processResponse(self, response):
        """
        Returns a dictionary representation of the response.
        Error: {'error': type(str), 'code': type(int)}
        Success: response.json()
        """
        # TODO: figure out errors or exceptions
        # should the error be an exception object?
        if response.status_code >= 200:
            # success codes should be handled here
            if response.status_code == 200:
                return response.json()
        if response.status_code >= 400:
            # default error. assumes the api returns error text as the body
            error = {
                'code': response.status_code,
                'error': response.text
            }
            if response.status_code == 404:
                error['error'] = "URL not found."
            return error

    def _composeURL(self, url, data):
        # TODO: pick replacement pattern and whether
        # to do named or ordered injection
        return url

    def _joinURL(self, a, b):
        """
        Returns a valid url after removing redundant forward slashes (/)
        """
        # this should guarantee that the output is a properly formed url
        # aka: http://google.com/ + /search == http://google.com/search
        # not http://google.com//search
        # someone has almost definitely written this well already.
        return a + b
