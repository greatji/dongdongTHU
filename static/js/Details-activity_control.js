/**
 * Created by hexiaohao on 2016/12/5.
 */

document.write("<script language=javascript src='static/js/config.js'></script>");

$.ajaxSetup ({
    cache: false //close AJAX cache
});

function param(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
}

var activityId = param('id');

$(document).ready(function () {
    $('#nav').load('/static/nav.html');
    $.ajax({
        type: 'POST',
        url: base_url + 'api/getActivity',
        contentType: 'application/json; charset=utf-8',
        data: '{"activityId":"' + activityId + '"}',
        dataType: 'json',
        success: function (data) {
            if (data['succeed']) {
                console.log(data['info']);
                activityDetails = new Vue({
                    el: '#activityDetails',
                    data: {
                        activity: data['info']
                    },
                    methods: {
                        joinActivityOrLogin: function () {
                            if (data['info']['identity'] == 'nobody') {
                                location.href = '/login.html';
                            } else {
                                $.ajax({
                                    type: 'POST',
                                    url: base_url + 'api/activity/addParticipant',
                                    contentType: 'application/json; charset=utf-8',
                                    data: JSON.stringify({
                                        activityId: activityId,
                                    }),
                                    dataType: 'json',
                                    success: function (data) {
                                        if (data['succeed']) {
                                            alert('succeed');
                                            location.reload();
                                        } else {
                                            alert(data['errmsg']);
                                            location.href = '/index.html'
                                        }
                                    }
                                });
                            }
                        },
                        quitActivity: function () {
                            $.ajax({
                                type: 'POST',
                                url: base_url + 'api/quitActivity',
                                contentType: 'application/json; charset=utf-8',
                                data: JSON.stringify({
                                    activityId: activityId,
                                }),
                                dataType: 'json',
                                success: function (data) {
                                    if (data['succeed']) {
                                        alert('succeed');
                                        location.reload();
                                    } else {
                                        alert(data['errmsg']);
                                        location.href = '/index.html'
                                    }
                                }
                            });
                        },
                        dissolveActivity: function () {
                            $.ajax({
                                type: 'POST',
                                url: base_url + 'api/deleteActivity',
                                contentType: 'application/json; charset=utf-8',
                                data: JSON.stringify({
                                    activityId: activityId,
                                }),
                                dataType: 'json',
                                success: function (data) {
                                    if (data['succeed']) {
                                        alert('succeed');
                                    } else {
                                        alert(data['errmsg']);
                                    }
                                    location.href = '/index.html'
                                }
                            });
                        },
                        showPersonalInfo: function (id) {
                            if (data['info']['identity'] == 'nobody') {
                                location.href = '/login.html';
                            } else if(data['info']['identity'] == 'non-participant') {
                                location.href = '/userInfo.html?id=' + id + '&full=false';
                            } else {
                                location.href = '/userInfo.html?id=' + id + '&full=true';
                            }
                        },
                        shareAlert: function (event) {
                            alert("请点击右上角分享")
                        }
                    },
                    computed: {
                        canJoinOrLogin: function () {
                            return data['info']['identity'] == 'non-participant' || data['info']['identity'] == 'nobody';
                        },
                        canQuit: function () {
                            return data['info']['identity'] == 'participant';
                        },
                        canDissolve: function () {
                            return data['info']['identity'] == 'organizer';
                        }
                    }
                });
            }
        }
    });
});



