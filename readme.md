# Example usage

Send a request

    ultima.network.endpoint()

Sends the previous request again

    ultima.network.endpoint.refresh()

if the next key was available, goes to the next page

    ultima.network.endpoint.next()

if the prev key was available, goes to the prev page

    ultima.network.endpoint.prev()

# Network options

## Required:

### baseUrl
The static portion of the network's api url.
can contain variables

### status_codes

Hash of success and failure codes

    {
        'success': [200,202],
        'failure': {
                    404: "URL not found.",
                    403: "Forbidden"
        }
    }

## Optional:

### headers
Dictionary of http headers

### auth
Auth settings.

### translations
Dictionary mapping Ultima terms to Network terms

#Endpoint options

##Required:

### url
url stub w/ variables using python named string replacement

### method
HTTP method for request

## Optional:

### headers
Dictionary of http headers to be added to network.headers

### nextKey
A key to find in the json data to the next page of results

### prevKey
A key to find in the json data to the prev page of results
