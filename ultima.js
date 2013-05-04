/*
Do we want to build the data enrichment into this? It could be, but
I think that a more generic approach would be for this application
to be ignorant of the schema of the data.  The complexity of this
module is already pretty high.  For this application to be ignorant
of the schema of the payloads, the other application has to be prepared
to process it. Do we want the enriched data to be part of the output
of our client? Does any other application need it? i can see both sides

Usage:
client = new UltimaSDK({'fbKeys':{...}, 'twitterKeys':{...},...});
client.facebook.posts(author="jhgaylor"); //wall posts
client.twitter.posts(author="jhgaylor"); //statuses
client.youtube.posts(author="jhgaylor"); //videos

client.network.comments(author="matt");

client.facebook.profile(user="jhgaylor")
client.twitter.profile(user="jhgaylor")
client.youtube.profile(user="jhgaylor")

client.facebook.photo(id=123) //media
client.instagram.photo(id=123) //media
client.twitter.photo(id=123) //media


client.facebook.feed(user="jhgaylor") //wall
client.youtube.feed(user="jhgaylor") //activities
client.twitter.feed(user="jhgaylor") // timeline

*/
//inclue npm packages
var $;
var _ = require('underscore');
var twitterlib = require('twitterlib');
var facebooklib = require('fb');

//include required client libraries
var FacebookSDK = function () {};   // https://developers.facebook.com/docs/reference/javascript/
var TwitterSDK = function () {};    // https://github.com/remy/twitterlib
//Api docs https://developers.google.com/youtube/v3/getting-started
var YoutubeSDK = function () {};    // https://developers.google.com/youtube/v3/libraries
//Instagram's current official library is in python https://github.com/Instagram/python-instagram
var InstagramSDK = function () {};  // https://github.com/Instagram/instagram-javascript-sdk/

var UltimaSDK = (function () {
    var UltimaSDK = {};
    //lazy load the client apis inside Ultima submodules
    var _facebook;
    var _twitter;
    var _youtube;
    var _instagram;
    var _google;
    var _linkedin;
    var _disqus;
    var _myspace;

    UltimaSDK.genericApiAdapter = function () {
        //I don't like my errors solution at all.  look around
        var genericError = function (level, code, message) {
            level = level || "log";
            code = code || 0;
            message = message || "Crickets";

            return {
                'level': level,
                'code': code,
                'message': message
            };
        };

        this.ForbiddenError = function () {
            return new genericError("Error", 403, "Access to api forbidden.");
        };

        this.OverQuotaError = function () {
            return new genericError("Error", 403, "API call limit exceeded.");
        };

        this.RateLimittedError = function () {
            return new genericError("Error", 403, "API rate limit exceeded. Please reduce frequency.");
        };
    };

    UltimaSDK.Ultima = function () {
        var that = this;
        this.facebook = (function () {
            /*
            All of these submodules are going to have to define a method for auth
            as well.  It should accept the required auth as arguments and auth should
            be handled transparently after that.

            each submodule should also return custom errors. the original error may be attached
            to the custom error. the errors are defined on genericApiAdapter in order to provide
            consistant errors across apis.

            have to come up with a way to paginate consistantly...
            */
            //lazy loading!
            _facebook = _facebook || facebooklib;

            var client = new UltimaSDK.genericApiAdapter();

            client.feed = function (username) {
                //we need an access token to make a call to /feed, so we need a dev token.
                var url = username+"/feed?access_token=BAACEdEose0cBAI92HfWY2V4ij9jbAulaZCnUZAD3bH4jgCyFp801leui5BhVEbzZBk7Y3BZBP8C332DZCB3XIZA3JKQ3BfiPWVJRvmC8y5Cz3WraObrgYNdbx8txkNzqqRmfYshcPKK03vRF6FjUerArOZBPBxvrS1zMAKZBhwLkhliRUfa6XJoOjYamfg5Xe3jZAMCxCc7lpvyApVURrw7fxgrP0iVGP0i0ZD";
                _facebook.api(url, function (res) {
                  if(!res || res.error) {
                   console.log(!res ? 'error occurred' : res.error);
                   return;
                  }
                  console.log(res);
                });
            };

            client.profile = function (username) {
                var url = username;
                _facebook.api(url, function (res) {
                  if(!res || res.error) {
                   console.log(!res ? 'error occurred' : res.error);
                   return;
                  }
                  console.log(res);
                });
            };
            return client;
        }());

        this.twitter = (function () {
            _twitter = _twitter || twitterlib;
            var client = new UltimaSDK.genericApiAdapter();
            client.posts = function () {
                /*
                This seems pretty cut and dry. if we need to write our own client
                libraries for these networks we totally can. Hell, it might be
                better for us to. Atleast this we are gaining familiarity with
                the limitations of the network's api.

                The purpose of each of these submodules is to contort the available
                api endpoints into information meaninful to us. We should only rewrite
                an available client library if it is less work than playing by their rules.
                */
                return _twitter.search("statuses", {'from': author});
            };

            client.feed = function (username) {
                twitterlib.timeline(username, function (tweets, options){
                    console.log(tweets);
                });
            };

            return client;
        }());

        this.youtube = (function () {
            _youtube = _youtube || new YoutubeSDK();
            var client = new UltimaSDK.genericApiAdapter();
            client.key = "value";

            client.profile = function () {
                return _youtube.search("profile", {'user': author});
            };

            return client;
        }());

        this.instagram = (function () {
            _instagram = _instagram || new InstagramSDK();
            var client = new UltimaSDK.genericApiAdapter();
            client.key = "value";

            client.profile = function () {
                return _instagram.search("profile", {'user': author});
            };

            return client;
        }());
    };

    return UltimaSDK.Ultima;
}($, _));

api = new UltimaSDK();
console.log(api);
api.twitter.feed("jhgaylor");
api.facebook.feed("jhgaylor");