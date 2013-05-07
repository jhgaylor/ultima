var $ = require('jquery');
var _ = require('underscore');

var UltimaSDK = (function (options) {

    var UltimaSDK = {};

    UltimaSDK.Ultima = function (options) {
        var that = this;
        options = UltimaSDK._cleanOptions(options);

        var _call = function () {
            return "this will make an http call";
        };

        this.setEndpoint = function (endpoint, options) {
            //parses the options for each network's details for a new function call
            //{'network_name': { 'option': 'value' } }
            for(var key in options) {
                var _endpoint = options[key]
                that[key][endpoint] = _call();
            }
            // _network[endpoint] = {};
        };

        for(var key in options) {
            that[key] = (function (options) {
                var _network = {};
                //console.log(options);

                return _network;
            }(options[key])); //find out if it's ALWAYS wrong to create a module in a loop, or if it's safe if we know what we're doing
        }

        // this.network = (function () {
        //     _network = {};

        //     var client = {};

        //     return client;
        // }());
    };

    UltimaSDK._cleanOptions = function (options) {
        return options;
    };

    return UltimaSDK.Ultima;
}($, _));

api = new UltimaSDK({
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
});


console.log(api);

api.setEndpoint('latest', {
    'tldr': {
        'url': "/tldrs/latest/",
        'method': "get",
        'headers': {},
        'nextKey': (void 0),
        'prevKey': (void 0)
    }
});
console.log(api.tldr.latest);

// console.log(api);
// api.twitter.feed("jhgaylor");
// api.facebook.feed("jhgaylor");
