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
        url: base_url + 'api/getClub',
        contentType: 'application/json; charset=utf-8',
        data: '{"clubId":"' + clubId + '"}',
        dataType: 'json',
        success: function (data) {
            clubDetails = new Vue({
                el: '#responseClub',
                data: {
                    leader: data['info']['leader'],
                    newId: '',
                    newName: '',
                },
                methods: {
                    changeClubLeader: function () {
                        var submitInfo = {
                            clubId: clubId,
                            leaderId: this.newId,
                            leaderName: this.newName,
                        };
                        $.ajax({
                            type: 'POST',
                            url: base_url + 'api/changeClubLeader',
                            contentType: 'application/json; charset=utf-8',
                            data: JSON.stringify(submitInfo),
                            dataType: 'json',
                            success: function (data) {
                                if (data['succeed']) {
                                    alert('操作成功');
                                    location.href = '/Details-club.html?id=' + clubId;
                                } else {
                                    alert(data['errmsg']);
                                }
                            }
                        });
                    },
                }
            });
        }
    });
});



