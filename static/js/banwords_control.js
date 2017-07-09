document.write("<script language=javascript src='static/js/config.js'></script>");

$.ajaxSetup ({
    cache: false //close AJAX cache
});

function param(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}

var clubId = param('id');

$(document).ready(function () {
    $('#nav').load('/static/nav.html');
    var clubDetails = new Vue({
        el: '#banwords',
        data: {
            banwords: '',
        },
        created: function () {
            this.getBannedWords();
        },
        methods: {
            getBannedWords: function () {
                $.ajax({
                    type: 'POST',
                    url: base_url + 'api/getBannedWords',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify({}),
                    dataType: 'json',
                    success: function (data) {
                        if (data['succeed']) {
                            clubDetails.banwords = data['info'].join('+');
                        } else {
                            alert(data['errmsg']);
                            location.href = '/index.html';
                        }
                    }
                });
            },
            setBannedWords: function () {
                $.ajax({
                    type: 'POST',
                    url: base_url + 'api/setBannedWords',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify({
                        bannedWords: clubDetails.banwords.split('+')
                    }),
                    dataType: 'json',
                    success: function (data) {
                        if (data['succeed']) {
                            alert('操作成功');
                        } else {
                            alert(data['errmsg']);
                        }
                    }
                });
            },
        }
    });
});



