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

    You will almost certainly not call this class manually.

    Self.session is an object that adheres the requests api
    the object should be an rauth instance if the server expects
    an oauth token
    """

    def __init__(self, baseUrl, headers, auth, status_codes):
        """
        configures client library
        """
        self.baseUrl = baseUrl  # the root of the target url
        self.headers = headers  # a dictionary of header key value pairs
        self.auth = None  # an auth object compatible with requests
        self.success_codes = status_codes['success']
        self.failure_codes = status_codes['failure']
        self.extras = {}
        self.debug = False

        # if necessary inflate auth from a dictionary to a session
        if auth['type'] == "oauth1":
            session = rauth.OAuth1Service(**auth['session'])
            self.session = session
        elif auth['type'] == "oauth2":
            session = rauth.OAuth2Service(**auth['session'])
            self.session = session
        else:
            self.session = requests

        # auth to be send via headers
        if auth['type'] == "headers":
            self.headers.update(auth['headers'])
        # auth to be send as extra data
        if auth['type'] == "apikey":
            self.extras.update(auth['apikey'])
        # auth object is HTTP Basic Authentication
        if auth['type'] == "basic":
            self.auth = tuple(auth['headers'])

    def call(self, partial_url, method, headers, data, url_vars, form_encoding):
        """
        Sends an authenticated request via the requests module.

        Returns a data or error dictionary
        """
        valid_methods = ["get", "post"]
        if method not in valid_methods:
            raise MissingHttpMethod
        url = self._composeURL(self._joinURL(self.baseUrl, partial_url),
                               url_vars
                               )
        response = None

        # combine to dictionaries without modifying either
        built_headers = dict(self.headers.items() + headers.items())

        auth = self.auth

        # inject data with extras (apikey auth)
        data.update(self.extras)

        # if the form needs to be sent as json data
        if form_encoding:
            data = json.dumps(data)
        # this is a call to a method of self. looks kinda wonky doesn't it?
        response = getattr(self, method)(url, data, built_headers, auth)

        if self.debug is True:
            print "DEBUG: Preposed url: %s" % url
            print "DEBUG: Client data: %s" % data
            print "DEBUG: Actual target url: %s" % response.url

        processed_response = self._processResponse(response)

        return processed_response

    def get(self, url, data, headers, auth):
        return self.session.get(url,
                                params=data,
                                headers=headers,
                                auth=auth
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

    def _joinURL(self, *args):
        """
        Returns a valid url after removing redundant forward slashes (/)
        """
        return "/".join([arg.strip("/") for arg in args])
