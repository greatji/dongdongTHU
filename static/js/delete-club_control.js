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
    $.ajax({
        type: 'POST',
        url:  base_url + 'api/getPersonalInfo',
        contentType: 'application/json; charset=utf-8',
        // data: '{"userId":"' + user_id + '"}',
        data: JSON.stringify({}),
        dataType: 'json',
        success: function (data) {
            if (data['succeed'] === false) {
                return
            }
            data = data['info'];
            var clubDetails = new Vue({
                el: '#deleteClub',
                data: {
                    deleteReason: ''
                },
                methods: {
                    deleteClub: function () {
                        $.ajax({
                            type: 'POST',
                            url: base_url + 'api/deleteClub',
                            contentType: 'application/json; charset=utf-8',
                            data: JSON.stringify({
                                clubId: clubId,
                                reason: this.deleteReason,
                                direct: data.state == 3
                            }),
                            dataType: 'json',
                            success: function (data) {
                                if (data['succeed']) {
                                    alert('操作成功');
                                } else {
                                    alert(data['errmsg']);
                                }
                                location.href = '/club-list.html'
                            }
                        });
                    },
                }
            });
        }
    });
});



