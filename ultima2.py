#import rauth


def _(s):
    return "_" + s


class Ultima(object):

    def __init__(self, options):
        for network, network_options in options.iteritems():
            self.__dict__[network] = Network(network_options)

    def setEndpoint(self, method, options):
        for network, network_options in options.iteritems():
            self.__dict__[network].setEndpoint(method, network_options)

    def _cleanOptions(self, options):
        # remove keys we aren't prepared to deal with
        return options


class Network(object):

    def __init__(self, options):
        for key, value in options.iteritems():
            self.__dict__[_(key)] = value

    def setEndpoint(self, method, options):
        pass

    def _cleanOptions(self, options):
        # remove keys we aren't prepared to deal with
        return options


class Endpoint(object):

    def __init__(self, options):
        for key, value in options.iteritems():
            if key == "headers":
                self.__dict__[_(key)].update(value)
            print key, value

    def _buildUrl(self):
        # how am I supposed to get to the network from here?
        # i need the base_url.  if i have to use python dunder
        # magic, then maybe i need to rethink my structure here.
        pass

    def _cleanResponse(self, response):
        """
        Returns a dictionary representation of the response.
        Error: {'error': type(str), 'code': type(int)}
        Success: response.json()
        """
        if response.status_code >= 200:
            #success codes should be handled here
            if response.status_code == 200:
                return response.json()
        if response.status_code >= 400:
            #default error. assumes the api returns error text as the body
            error = {
                'code': response.status_code,
                'error': response.text
            }
            if response.status_code == 404:
                error['error'] = "URL not found."
            return error



ultima_options = {
    'tldr': {
        'baseUrl': "https://api.tldr.io",
        'headers': {},
        'auth': {
            'type': 'headers',
            'header': {
                'name': 'jakegaylor',
                'key': "09fd8c39ae32ccf8e6ac8"
            }
        }
    }
}

latest_endpoint = {
    'tldr': {
        'url': "/tldrs/latest/",
        'method': "get",
        'headers': {},
        'nextKey': None,
        'prevKey': None
    }
}

ultima = Ultima(ultima_options)

ultima.setEndpoint('latest', latest_endpoint)
print ultima.__dict__
for k, v in ultima.__dict__.iteritems():
    print v.__dict__

# for k, v in ultima_options.iteritems():
#     print k, v


# starClient = Ultima(ultima_options)
