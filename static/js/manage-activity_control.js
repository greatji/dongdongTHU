/**
 * Created by hexiaohao on 2016/12/5.
 */

document.write("<script language=javascript src='static/js/config.js'></script>");

$.ajaxSetup({
    cache: false //close AJAX cache
});

var app = new Vue({
    el: '#manage_activity',
    data: {
        activitys: [],
        cur_act: 1,
        is_su: false,
    },
    methods: {
        showActivityInfo: function(id) {
            console.log('/Details-activity.html?id=' + id);
            location.href = '/Details-activity.html?id=' + id;
        },
        topActivity: function(id, istop) {
            $.ajax({
                type: 'POST',
                url: base_url + 'api/activity/top',
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify({
                    activityId: id,
                    top: ! + istop,
                }),
                dataType: 'json',
                success: function(data) {
                    if (data['succeed']) {
                        alert('操作成功');
                    } else {
                        alert(data['errmsg']);
                    }
                    location.href = '/manage-activity.html'
                }
            });
        },
        deleteActivity: function(id) {
            location.href = '/delete-activity.html?id=' + id;
        },
    }
});

$(document).ready(function() {
    $('#nav').load('/static/nav.html');
    $.ajax({
        type: 'POST',
        url: base_url + 'api/listActivities',
        data: '{}',
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
        data: '{}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data) {
            if (data['succeed']) {
                if (data.info.state == 3) showAdmin();
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

