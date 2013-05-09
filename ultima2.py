import rauth
from httpclient import HttpClient


def _(s):
    return "_" + s


class Ultima(object):
    """
    A Common interface for creating networks and endpoints.
    Public API is only the available networks

    Iteration returns networks
    """
    def __init__(self, options):
        """
        Create a network w/ options for each key, value
        pair in options.
        """
        if not self._verifyOptions(options):
            raise Exception

        for network, network_options in options.iteritems():
            setattr(self, network, Network(network_options))

    def __iter__(self):
        """
        Iterable to make it easy to call .endpoint of every network
        """
        for key, value in self.__dict__.iteritems():
            yield value

    def setEndpoint(self, options):
        """
        Create an endpoint on each network w/ options for each key.
        { method: { network1: {options}, network2: {options} }
        """
        for method, networks in options.iteritems():
            for network, network_options in networks.iteritems():
                getattr(self, network).setEndpoint(method, network_options)

    def _verifyOptions(self, options):
        """
        Raise exeption if options contains an invalid key.
        """
        reserved_words = ["and", "del", "for", "is", "raise", "assert",
                          "elif", "from", "lambda", "return", "break",
                          "else", "global", "not", "try", "class", "except",
                          "if", "or", "while", "continue", "exec", "import",
                          "pass", "yield", "def", "finally", "in", "print"
                          ]
        for key in options:
            if key in reserved_words:
                return False
        return True


class Network(object):
    """
    An object containing a custom http client and callables
    representing the endpoints for the network.
    Public API is all available endpoints and a psuedo private
    custom HttpClient.
    """

    def __init__(self, options):
        self._client = HttpClient(baseUrl=options['baseUrl'],
                                  headers=options['headers'],
                                  auth=options['auth']
                                  )

    def __iter__(self):
        """
        Iterable to be consistant with Ultima
        """
        for key, value in self.__dict__.iteritems():
            if key[0] != "_":
                yield value

    def setEndpoint(self, method, endpoint_options):
        """ Assign a callable to the endpoint name """
        setattr(self, method, Endpoint(self._client, endpoint_options))

    def _verifyOptions(self, options):
        """
        Raise exeption if options contains an invalid key.
        """
        return options


class Endpoint(object):

    def __init__(self, client, options):
        self.client = client

        for key, value in options.iteritems():
            setattr(self, key, value)

    # this is the entry point for url and data params
    # do call as star.network.endpoint(url_params={}, **kwargs)
    def __call__(self, *args, **kwargs):
        params = self._translate(kwargs)
        self._last_args = [self.url, self.method, self.headers, params]
        return self.refresh()

    def next(self):
        self._last_args = [self._next_url, self.method, self.headers, {}]
        return self.refresh()

    def prev(self):
        self._last_args = [self._prev_url, self.method, self.headers, {}]
        return self.refresh()

    def refresh(self):
        """
        Sends the last request again.
        """
        response = self.client.call(*self._last_args)
        processed_response = self._processResponse(response)
        return processed_response

    def _processResponse(self, response):
        # this is where an error from HttpClient would propogate
        # unless we use exceptions, then it's already dealt with
        # check for next key
        # if response[self.next_key]:
        #    self._next_url = response[self.next_key]
        # check for prev key
        # if response[self.prev_key]:
        #    self._prev_url = response[self.prev_key]
        pass

    def _translate(self, options):
        # used to change the common names for arguments to endPoint()
        # into the names specific to this network
        return options


# TODO: find a place for translation dictionaries.
# this should be network wide
ultima_options = {
    'tldr': {
        'baseUrl': "https://api.tldr.io",
        'headers': {},
        'auth': {
            'type': 'headers',
            'headers': {
                'name': 'jakegaylor',
                'key': "09fd8c39ae32ccf8e6ac8"
            }
        }
    },
    'codegurus': {
        'baseUrl': "https://api.codegurus.io",
        'headers': {},
        'auth': {
            'type': 'headers',
            'headers': {
                'name': 'tester',
                'key': "09fd8c39ae32ccf8e6ac8"
            }
        }
    }
}


endpoint_options = {
    'latest': {
        'tldr': {
            'url': "/tldrs/latest/",
            'method': "get",
            'headers': {},
            'nextKey': None,
            'prevKey': None
        },
        'codegurus': {
            'url': "/latest/",
            'method': "get",
            'headers': {},
            'nextKey': None,
            'prevKey': None
        }
    },
    'posts': {
        'tldr': {
            'url': "/tldrs/posts/",
            'method': "get",
            'headers': {},
            'nextKey': None,
            'prevKey': None
        },
        'codegurus': {
            'url': "/posts/",
            'method': "get",
            'headers': {},
            'nextKey': None,
            'prevKey': None
        }
    }
}


ultima = Ultima(ultima_options)
ultima.setEndpoint(endpoint_options)

# print [key for key in ultima.tldr.__dict__]
print ultima.tldr.__dict__
print [i for i in ultima.tldr]
# print ultima.tldr.posts()
# print ultima.tldr.latest()

## Example
# ultima.network.endpoint()
# sends the preview request again
# ultima.network.endpoint.refresh()
# if the next key was available, goes to the next page
# ultima.network.endpoint.next()
# if the prev key was available, goes to the prev page
# ultima.network.endpoint.prev()
