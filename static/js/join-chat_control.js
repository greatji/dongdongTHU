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
                location.href = '/login.html';
                return
            }
            activityDetails = new Vue({
                el: '#activity_chat',
                data: {
                    user:data['info'],
                    comments: [],
                    content: '',
                    activityId: activityId,
                },
                created: function () {
                    this.getComment();
                },
                methods: {
                    showPersonalInfo: function (id) {
                        location.href = '/userInfo.html?id=' + id;
                    },
                    addComment: function () {
                        if (this.content == '') return;
                        $.ajax({
                            type: 'POST',
                            url: base_url + 'api/activity/addComment',
                            contentType: 'application/json; charset=utf-8',
                            data: JSON.stringify({
                                activityId: activityId,
                                content: activityDetails.content
                            }),
                            dataType: 'json',
                            success: function (data) {
                                if (data['succeed']) {
                                    activityDetails.getComment();
                                    activityDetails.content = '';
                                } else {
                                    alert(data['errmsg']);
                                    location.href = '/index.html'
                                }
                            }
                        });
                    },
                    getComment: function () {
                        $.ajax({
                            type: 'POST',
                            url: base_url + 'api/activity/getComment',
                            contentType: 'application/json; charset=utf-8',
                            data: JSON.stringify({
                                activityId: activityId,
                            }),
                            dataType: 'json',
                            success: function (data) {
                                if (data['succeed']) {
                                    console.log(data['info']);
                                    activityDetails.comments = data['info'];
                                    activityDetails.$nextTick(function () {
                                        var div = document.getElementById("chat");
                                        console.log(div);
                                        div.scrollTop = div.scrollHeight - div.clientHeight;
                                    })
                                }
                            }
                        });
                    }
                }
            });
        }
    });
});



