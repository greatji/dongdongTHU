/**
 * Created by hexiaohao on 2016/12/5.
 * Modified by Dash Chen on 2017/06.
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
            if (data.state == 3) showAdmin();
        }
    });
    $.ajax({
        type: 'POST',
        url: base_url + 'api/getActivity',
        contentType: 'application/json; charset=utf-8',
        data: '{"activityId":"' + activityId + '"}',
        dataType: 'json',
        success: function (data) {
            if (data['succeed']) {
                console.log(data['info']);
                document.title = '咚咚体育平台 | ' + data.info.name + ' | ' + data.info.type[0];
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
                                            alert('操作成功');
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
                                        alert('操作成功');
                                        location.reload();
                                    } else {
                                        alert(data['errmsg']);
                                        location.href = '/index.html'
                                    }
                                }
                            });
                        },
                        deleteActivity: function () {
                            if (confirm('确认删除吗？')) {
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
                                            alert('操作成功');
                                        } else {
                                            alert(data['errmsg']);
                                        }
                                        location.href = '/index.html'
                                    }
                                });
                            };
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
                        canDelete: function () {
                            return data['info']['identity'] == 'organizer';
                        }
                    }
                });
            }
        }
    });
});



