#What is it?
A tool to process json into an api client

#Why do I want it?

It's going to save you alot of time in the long term. One json document can describe the server implementation of the api while allowing the client to be built pretty much however.

Talk about how cool it will be to have providers describing their network and being able to create a custom client from json input in any language

## Example usage

	#Send a request
    ultima.network.endpoint()

	#Sends the previous request again
    ultima.network.endpoint.refresh()

	#if the next key was available, goes to the next page
    ultima.network.endpoint.next()

	#if the prev key was available, goes to the prev page
    ultima.network.endpoint.prev()

### Network options

#### Required:
--------------
##### baseUrl
The static portion of the network's api url.
can contain variables

##### status_codes

Hash of success and failure codes

Success codes will return the object from the json of the response body.

    {
        'success': [200,202],
        'failure': {
                    404: "URL not found.",
                    403: "Forbidden"
        }
    }

#### Optional:
--------------
##### headers
Dictionary of http headers

##### auth
Auth settings.

##### translations
Dictionary mapping Ultima terms to Network terms

##Endpoint options

####Required:
-------------
##### url
url stub w/ variables using python named string replacement

##### method
HTTP method for request

#### Optional:
--------------
##### headers
Dictionary of http headers to be added to network.headers

##### url_defaults
Dictionary of default url parameter values

##### form_encoding
Defaults to true.  set false to send json string instead

##### nextKey
A key to find in the json data to the next page of results

##### prevKey
A key to find in the json data to the prev page of results
