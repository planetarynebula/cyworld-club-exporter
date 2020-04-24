/**
 * Created by ecst_000 on 2016-01-10.
 */
module.exports = function (cookies, articles, callback) {
    var cheerio = require('cheerio');
    var $ = cheerio.load(articles);
	var fs = require('fs');
    var itemList = $('table.board_type_tbl.board_member .col_title a, table.board_type_tbl.board_admin .col_title a');
    var maxPage = 0;

    var maxPageCatch = /cpage=([0-9]+)/g.exec($('a.btn.last_page').attr('href'));
    if (null !== maxPageCatch) {
        maxPage = parseInt(maxPageCatch[1]);
    } else {
        maxPage = $('.wrap_paging').children('a').length + 1;
    }

    var result = {
        maxPage: maxPage,
        articles:[]
    };
    for (var i = 0; i < itemList.length; i++) {
        var el = itemList[i];
        var link = /item_seq=([0-9]+)/g.exec(el.attribs.onclick);

        result.articles.push(parseInt(link[1]));
    }

    callback(null, cookies, result);
};