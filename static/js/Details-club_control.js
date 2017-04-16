/**
 * Created by hexiaohao on 2016/12/4.
 */

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
            if (data['succeed']) {
                console.log(data['info']);
                var clubDetails = new Vue({
                    el: '#clubDetails',
                    data: {
                        club: data['info']
                    },
                    methods: {
                        joinClubOrLogin: function () {
                            if (data['info']['identity'] == 'non-member') {
                                $.ajax({
                                    type: 'POST',
                                    url: base_url + 'api/joinClub',
                                    contentType: 'application/json; charset=utf-8',
                                    data: JSON.stringify({
                                        clubId: data['info']['id'],
                                    }),
                                    dataType: 'json',
                                    success: function (data) {
                                        if (data['succeed']) {
                                            alert('请等待管理员审核');
                                            location.reload();
                                        } else {
                                            alert(data['errmsg']);
                                            location.href = '/club-list.html'
                                        }
                                    }
                                });
                            } else {
                                location.href = '/login.html';
                            }
                        },
                        quitClub: function () {
                            $.ajax({
                                type: 'POST',
                                url: base_url + 'api/quitClub',
                                contentType: 'application/json; charset=utf-8',
                                data: JSON.stringify({
                                    clubId: data['info']['id'],
                                }),
                                dataType: 'json',
                                success: function (data) {
                                    if (data['succeed']) {
                                        alert('succeed');
                                        location.reload();
                                    } else {
                                        alert(data['errmsg']);
                                        location.href = '/club-list.html'
                                    }
                                }
                            });
                        },
                        dissolveClub: function () {
                            $.ajax({
                                type: 'POST',
                                url: base_url + 'api/deleteClub',
                                contentType: 'application/json; charset=utf-8',
                                data: JSON.stringify({
                                    clubId: data['info']['id'],
                                }),
                                dataType: 'json',
                                success: function (data) {
                                    if (data['succeed']) {
                                        alert('succeed');
                                    } else {
                                        alert(data['errmsg']);
                                    }
                                    location.href = '/club-list.html'
                                }
                            });
                        },
                        showPersonalInfo: function (id) {
                            if (data['info']['identity'] == 'nobody') {
                                location.href = '/login.html';
                            } else if(data['info']['identity'] == 'non-member') {
                                location.href = '/userInfo.html?id=' + id + '&full=false';
                            } else {
                                location.href = '/userInfo.html?id=' + id + '&full=true';
                            }
                        },
                    },
                    computed: {
                        canJoinOrLogin: function () {
                            return data['info']['identity'] == 'non-member' || data['info']['identity'] == 'nobody';
                        },
                        canQuit: function () {
                            return data['info']['identity'] == 'member';
                        },
                        canDissolve: function () {
                            return data['info']['identity'] == 'leader';
                        }
                    }
                });
            }
        }
    });
});
