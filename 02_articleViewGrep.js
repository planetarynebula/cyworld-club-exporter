/**
 * Created by ecst_000 on 2016-01-09.
 */
var async = require('async');
var cheerio = require('cheerio');
var fs = require('fs');
var config = require('./core/config');
var articleId = [];
var ProgressBar = require('progress');

async.waterfall([
    // get list
    function (callback) {
        console.log('get article list');
        fs.readdir('./result/', callback);
    },

    function (list, callback) {
        var queue = [];
        for (var i in list) {
            var entry = list[i];
            if ('article_list' === entry.substr(0, 12)) {
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
                console.log('articles done');
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
        var bar = new ProgressBar(' downloading [:bar] :rate/bps :percent :etas', { 
            complete: '=',
            incomplete: ' ',
            width: 50,
            total: articleId.length
        });
        async.eachSeries(
            articleId,
            function (articleNo, next) {
				try {
					if(!fs.accessSync('result/article_view_' + articleNo + '.txt')) {
                        bar.interrupt('skip article - ' + articleNo);
                        bar.tick();
						return next();
					}
				} catch(e) {
				}
                async.waterfall([
                    function (subroutine) {
                        bar.interrupt('download article - ' + articleNo);
                        require('./core/articleView')(cookies, config.clubId, articleNo, subroutine);
                    },

                    function (cookies, articleNo, data, subroutine) {
                        bar.interrupt('parsing article - ' + articleNo);
                        require('./core/parseArticleView')(cookies, articleNo, data, subroutine);
                    },

                    function (cookies, articleNo, contents) {
                        fs.writeFile('result/article_view_' + articleNo + '.txt', JSON.stringify(contents), function(err) {
                            if (err) {
                                bar.interrupt('error: cannot write article ' + articleNo);
                                console.dir(err);
                                return;
                            }
                            bar.interrupt('success to write article ' + articleNo);
                        });
                        setTimeout(next, config.sleep);
                        bar.tick();
                    }
                ]);
            },

            function () {
                console.log('articles done');
            }
        );
    }
]);