/**
 * Created by ecst_000 on 2016-01-09.
 */
var async = require('async');
var fs = require('fs');
var cheerio = require('cheerio');
var config = require('./core/config');

var articleId = [];

async.waterfall([
    // get list
    function (callback) {
        console.log('get galleries list');
        fs.readdir('./result/', callback);
    },

    function (list, callback) {
        var queue = [];
        for (var i in list) {
            var entry = list[i];
            if ('gallery_list' === entry.substr(0, 12)) {
                queue.push(entry);
            }
        }

        callback(null, queue);
    },


    function (queue, callback) {
        async.eachSeries(
            queue,
            function (filename, next) {
                async.waterfall([
                    function (subroutine) {
                        fs.readFile('./result/' + filename, 'utf8', subroutine);
                    },

                    function (data) {
                        articleId = articleId.concat(JSON.parse(data));
                        next();
                    }
                ]);
            },
            function () {
                console.log('galleries done');
                callback();
            }
        );
    },


    // get auth
    function (callback) {
        console.log('get auth');
        require('./core/auth')(config.userId, config.password, config.rsaPublic, config.rsaModulus,
            callback);
    },

    // paring cookie
    function (cookies, callback) {
        console.log('paring cookies');
        var cookieLength = cookies.length;
        var newCookie = [];
        for (var i = 0; i < cookieLength; i++) {
            var chuck = cookies[i];
            newCookie.push(chuck.substring(0, chuck.indexOf('; ')));
        }

        callback(null, newCookie.join('; '));
    },

    function (cookies) {
        async.eachSeries(
            articleId,
            function (articleNo, next) {
                async.waterfall([
                    function (subroutine) {
                        console.log('download article - ' + articleNo);
                        require('./core/galleryView')(cookies, config.clubId, articleNo, subroutine);
                    },

                    function (cookies, articleNo, data, subroutine) {
                        console.log('parsing article - ' + articleNo);
                        require('./core/parseGalleryView')(cookies, articleNo, data, subroutine);
                    },

                    function (cookies, articleNo, contents) {
                        fs.writeFile('result/gallery_view_' + articleNo + '.txt', JSON.stringify(contents), function(err) {
                            if (err) {
                                console.log('error: cannot write gallery ' + articleNo);
                                console.dir(err);
                                return;
                            }
                            console.log('success to write gallery ' + articleNo);
                        });
                        setTimeout(next, config.sleep);
                    }
                ]);
            },

            function () {
                console.log('galleries done');
            }
        );
    }
]);