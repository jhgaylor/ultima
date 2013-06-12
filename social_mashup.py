from ultima.ultima import Ultima

network_options = {
    'facebook': {
        'baseUrl': "https://graph.facebook.com/",
        'headers': {},
        'auth': {
            "type": "apikey",
            "apikey": {
                "access_token": "CAACEdEose0cBANZC54JUbf1crykc28FtI0I5dn1wW0swRyH2Q81zI3VCU2qNmOt1tdV6gvvZCUYb7j7QpxDPEQiPkzLHlZCCWKbNZAhEsKqzZA2eO1eYkIi9ekXKpXnsaakToDFC8Amtr36w8nYU9o5jefTaru0MZD"
            }
        },
        'status_codes': {
            'success': [200],
            'failure': {
                404: "URL not found"
            }
        },
        'translations': {
            'user': 'userid'
        }
    },
    'twitter': {
        'baseUrl': "https://api.twitter.com/1.1/",
        'headers': {},
        'auth': {
            "type": "headers",
            "headers": {}
        },
        'status_codes': {
            'success': [200],
            'failure': {
                404: "URL not found"
            }
        },
        'translations': {
            'user': 'screen_name'
        }
    },
    'instagram': {
        'baseUrl': "https://api.instagram.com/v1/",
        'headers': {},
        'auth': {
            "type": "apikey",
            "apikey": {
                "access_token": "405778445.90cbda8.c0a7546747634555aa4da5f56ac02297",
                "client_id": "90cbda8186814acea5e93f960f569844"
            }
        },
        'status_codes': {
            'success': [200],
            'failure': {
                404: "URL not found"
            }
        },
        'translations': {
            'user': 'userid'
        }
    }
}

endpoint_options = {
    'profile': {
        'facebook': {
            'url': "/%(userid)s/",
            'url_defaults': {
                'userid': 'me'
            },
            'form_encoding': False,
            'method': "get",
            'nextKey': None,
            'prevKey': None
        }
    },
    'feed': {
        'facebook': {
            'url': "/%(userid)s/feed",
            'url_defaults': {
                'userid': 'me'
            },
            'form_encoding': False, # this also needs to be here.
            'method': "get", # don't forget to set this
            'nextKey': None,
            'prevKey': None
        },
        'twitter': {
            'url': "/statuses/user_timeline.json",
            'url_defaults': {},
            'form_encoding': False, # this also needs to be here.
            'method': "get", # don't forget to set this
            'nextKey': None,
            'prevKey': None
        },
        'instagram': {
            'url': "/users/feed",
            'url_defaults': {},
            'form_encoding': False, # this also needs to be here.
            'method': "get", # don't forget to set this
            'nextKey': None,
            'prevKey': None
        }
    },
    'pictures': {
        'instagram': {
            'url': "/users/%(userid)s/media/recent",
            'url_defaults': {
                'userid': "me"
            },
            'form_encoding': False, # this also needs to be here.
            'method': "get", # don't forget to set this
            'nextKey': None,
            'prevKey': None
        }
    }
    # 'friends': {
    #     'facebook': {
    #         'url': "/%(userid)s/friends/",
    #         'url_defaults': {
    #             'userid': 'me'
    #         },
    #         'method': "",
    #         'nextKey': None,
    #         'prevKey': None
    #     }
    # },
    # posts
    # activities?
    # likes
    # statuses
    # interests
}

client = Ultima(network_options)
client.facebook._client.debug = True
client.twitter._client.debug = True
client.instagram._client.debug = True
client.setEndpoint(endpoint_options)

resp = client.facebook.feed(user='dumbbyte')
# resp = client.twitter.feed(user="jhgaylor")
#resp = client.instagram.pictures(user=1574083)
#resp = client.instagram.pictures({"user":"405778445"})  # jhgaylor

print resp
