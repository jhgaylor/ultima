from ultima.ultima import Ultima

network_options = {
    'facebook': {
        'baseUrl': "https://graph.facebook.com/",
        'headers': {},
        'auth': {
            "type": "apikey",
            "apikey": {
                "access_token": "CAACEdEose0cBAMCAZCRCZAub52ghQnpbMznDHxaRvnFqyms1vWDB7UF7NFGEq1xCsGW0RN1CgvzOqCbp5mLHCjNn0qZB63zHTBPbUZAQDmmgP6CdVbehUJXb4YH2CZBNjcxVOCRursGfZAW2R2MsfiHc43Ini5GBPDPNpvHUTSuAZDZD"
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
        'baseUrl': "https://api.twitter.com/1/",
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
            'form_encoding': False, #this also needs to be here.
            'method': "get", #don't forget to set this
            'nextKey': None,
            'prevKey': None
        },
        'twitter': {
            'url': "/statuses/user_timeline.json",
            'url_defaults': {},
            'form_encoding': False, #this also needs to be here.
            'method': "get", #don't forget to set this
            'nextKey': None,
            'prevKey': None
        }
    },
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
client.setEndpoint(endpoint_options)

# resp = client.facebook.feed({'user': 'dumbbyte'})
resp = client.twitter.feed(user="jhgaylor")
print resp
