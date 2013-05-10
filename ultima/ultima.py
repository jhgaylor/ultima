from .httpclient import HttpClient


def _(s):
    return "_" + s


class RequiredField(Exception):
    """
    This field is required for instantiation
    """


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
    Public API is all available endpoints and psuedo privates
    _client (a custom HttpClient) and _translations (a dictionary
    to map network specific terminology to Ultima terms).
    """

    def __init__(self, options):
        self._client = HttpClient(baseUrl=options['baseUrl'],
                                  headers=options['headers'],
                                  auth=options['auth'],
                                  status_codes=options['status_codes']
                                  )
        if 'translations' in options:
            self._translations = options['translations']
        else:
            self._translations = {}

    def __iter__(self):
        """
        Iterable to be consistant with Ultima
        """
        for key, value in self.__dict__.iteritems():
            if key[0] != "_":
                yield value

    def setEndpoint(self, method, endpoint_options):
        """ Assign a callable to the endpoint name """
        endpoint_options.update({'_translations': self._translations})
        setattr(self, method, Endpoint(self._client, endpoint_options))

    def _verifyOptions(self, options):
        """
        Raise exeption if options contains an invalid key.
        """
        return options


class Endpoint(object):

    def __init__(self, client, options):
        self.client = client
        self.optional_fields = {
            'field': "default_value",
            'field2': {},
        }
        self.required_fields = ['required_field']

        for key, value in options.iteritems():
            setattr(self, key, value)

    def _fillDefaults(self, options):
        """
        Raises an exception if a required field is empty.
        Prefills sane defaults for optional fields
        """
        for field, value in self.optional_fields.iteritems():
            if field not in options:
                options[field] = value

        for field, value in self.required_fields.iteritems():
            if field not in options:
                raise RequiredField

        return options

    def __call__(self, *args, **kwargs):
        """
        this is the entry point for url and data params
        optional unnamed parameter for url composition
        do call as star.network.endpoint({'url_param1':"value"}, **kwargs)
        """
        params = self._translate(kwargs)

        if len(args) > 0:
            url_params = self._translate(args[0])
        else:
            url_params = self.url_defaults

        print params
        self._last_args = [self.url,
                           self.method,
                           self.headers,
                           params,
                           url_params
                           ]
        return self.refresh()

    def next(self):
        self._last_args = [self._next_url, self.method, self.headers, {}, {}]
        return self.refresh()

    def prev(self):
        self._last_args = [self._prev_url, self.method, self.headers, {}, {}]
        return self.refresh()

    def refresh(self):
        """
        Sends the last request again.
        """
        response = self.client.call(*self._last_args)
        processed_response = self._processResponse(response)
        return processed_response

    def _processResponse(self, response):
        """
        Update state from response
        """
        if self.nextKey in response:
            self._next_url = response[self.next_key]
        if self.prevKey in response:
            self._prev_url = response[self.prev_key]
        return response

    def _translate(self, options):
        """
        used to change the Ultima terms for arguments
        into the terms specific to this network
        """
        translated_options = {}
        for options_key, value in options.iteritems():
            new_key = options_key
            if options_key in self._translations:
                new_key = self._translations[options_key]
            translated_options.update({new_key: value})
        return translated_options
