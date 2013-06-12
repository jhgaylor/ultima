#Changes not reflected in document

URL parameters and data payload are all **kwargs of endpoint.call.  they are seperated within the method using the values in self.url_defaults

If you manually set ultima.network.endpoint._normalizer to a callable then essentially

    ultima.network.endpoint()

becomes

    ultima.network.endpoint._normalizer(ultima.network.endpoint())

#What is it?

A tool to process json into an api client

#Why do I want it?

It's going to save you alot of time in the long term. One json document can describe the server implementation of the api while allowing the client to be built pretty much however.

Think about how cool it will be to have providers describing their network and being able to create a custom client from json input in any language for which this tool is available.

## Example usage
----------------
    #import the client
    from ultima.ultima import Ultima

    #instatiate a client
    ultima = Ultima(network_options)

	#Send a request
    ultima.network.endpoint()

	#Sends the previous request again
    ultima.network.endpoint.refresh()

	#if the next key was available, goes to the next page
    ultima.network.endpoint.next()

	#if the prev key was available, goes to the prev page
    ultima.network.endpoint.prev()

### Network options
Example

    network_options = {
        'tldr': {
            'baseUrl': "https://api.tldr.io",
            'headers': {},
            'auth': {
                'type': 'headers',
                'headers': {
                    'name': 'username',
                    'key': "key"
                }
            },
            'status_codes': {
                'success': [200],
                'failure': {
                    404: "URL not found"
                }
            },
            'translations': {
                #key, value = Ultima term, Network specific term
                'rpp': "number",
                'user': "username"
            }
        }
    }



#### Required:
--------------
**baseUrl** -- *The static portion of the network's api url and can contain variables*

**status_codes** -- *Hash of success and failure codes.  Success codes will return the object from the json of the response body.*


#### Optional:
--------------
**headers** -- *Dictionary of http headers*

**auth** -- *Auth settings.*

**translations** -- *Dictionary mapping Ultima terms to Network terms*

### Endpoint options

    endpoint_options = {
        'getLatestTldrs': {
            'tldr': {
                'url': "/tldrs/latest/%(number)s",
                'url_defaults': {
                    'number': 10
                },
                'method': "get",
                'headers': {},
                'nextKey': None,
                'prevKey': None
            },
        },
        'searchByUrl': {
            'tldr': {
                'url': "/tldrs/search/",
                'method': "get",
                'headers': {},
                'nextKey': None,
                'prevKey': None
            },
        },
        ...
    }

####Required:
-------------
**url** -- *url stub w/ variables using python named string replacement*

**method** -- *HTTP method for request*

#### Optional:
--------------
**headers** -- *Dictionary of http headers to be added to network.headers*

**url_defaults** -- *Dictionary of default url parameter values*

**form_encoding** -- *Defaults to true.  set false to send json string instead*

**nextKey** -- *A key to find in the json data to the next page of results*

**prevKey** -- *A key to find in the json data to the prev page of results*
