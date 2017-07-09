/**
 * Created by hexiaohao on 2016/12/5.
 */

document.write("<script language=javascript src='static/js/config.js'></script>");

$.ajaxSetup({
    cache: false //close AJAX cache
});

function param(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
}

var user_id = param('id');

var app = new Vue({
    el: '#manage_user_detail',
    data: {
        activitys: [],
        user: {},
        level: 0
    },
    methods: {
        showActivityInfo: function(id) {
            console.log('/Details-activity.html?id=' + id);
            location.href = '/Details-activity.html?id=' + id;
        },
        changeState: function() {
            var submitInfo = {
                studentId: this.user.id,
                level: this.level,
            };
            $.ajax({
                type: 'POST',
                url: base_url + 'api/changeUserLevel',
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify(submitInfo),
                dataType: 'json',
                success: function(data) {
                    if (data['succeed']) {
                        alert('操作成功');
                    } else {
                        alert(data['errmsg']);
                    }
                }
            });
        },
        toImageName: function(type) {
            switch (type) {
                case "全部":
                    return "kind_all";
                case "羽毛球":
                    return "kind_01";
                case "篮球":
                    return "kind_02";
                case "跑步":
                    return "kind_03";
                case "游泳":
                    return "kind_04";
                case "健身":
                    return "kind_05";
                case "乒乓球":
                    return "kind_06";
                case "足球":
                    return "kind_07";
                case "网球":
                    return "kind_08";
                case "冰雪":
                    return "kind_09";
                case "其它":
                    return "kind_other";
            }
        }
    },
});

$(document).ready(function() {
    $('#nav').load('/static/nav.html');
    $.ajax({
        type: 'POST',
        // TODO: 获取指定用户的所有活动
        url: base_url + 'api/listActivities',
        data: JSON.stringify({userId:user_id}),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data) {
            if (data['succeed']) {
                app.activitys = data['info'];
            }
        }
    });
    $.ajax({
        type: 'POST',
        url: base_url + 'api/getPersonalInfo',
        data: JSON.stringify({studentId:user_id, full:true}),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data) {
            if (data['succeed']) {
                app.user = data['info'];
                if (app.user.state == 3) app.level = 3;
                else if (app.user.state == 2 && app.user.president.length == 0) app.level =  0;
                else app.level = 1;
            }
        }
    });
});

function setTab(name, cursel, n) {
    app.cur_act = cursel;
    for (i = 1; i <= n; i++) {
        var menu = document.getElementById(name + i);
        if (menu) menu.className = ((i == cursel) ? "hover" : "");
    }
}
