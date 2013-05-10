import json
from ultima.ultima import Ultima

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
    'searchBatch': {
        'tldr': {
            'url': "/tldrs/searchBatch/",
            'method': "post",
            'form_encoding': False,
            'nextKey': None,
            'prevKey': None
        },
    },
    'getUser': {
        'tldr': {
            'url': "/users/%(username)s/",
            'method': "get",
            'nextKey': None,
            'prevKey': None
        },
    },
    'getUserTldrs': {
        'tldr': {
            'url': "/users/%(username)s/tldrsCreated",
            'method': "get",
            'nextKey': None,
            'prevKey': None
        },
    },
    'getCategories': {
        'tldr': {
            'url': "/categories/",
            'method': "get",
            'nextKey': None,
            'prevKey': None
        },
    }

}


ultima = Ultima(network_options)
ultima.setEndpoint(endpoint_options)

#example of url parameters
print ultima.tldr.getLatestTldrs({'rpp': 1})

# #example of payload
# ultima.tldr.searchByUrl(url="http://tldr.io")

# #example of payload
# ultima.tldr.searchBatch(batch=["http://tldr.io",
#                                "http://news.ycombinator.com/"
#                                ]
#                         )

# #example of url parameters
# ultima.tldr.getUser({'username': "jhgaylor"})

# #example of url parameters
# ultima.tldr.getUserTldrs({'username': "jhgaylor"})

# #example w/o parameters
# ultima.tldr.getCategories()

# #example of payload
# ultima.tldr.getLatestTldrs(category="tech-news")
