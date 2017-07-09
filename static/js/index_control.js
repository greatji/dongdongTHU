/**
 * Created by hexiaohao on 2016/12/5.
 */

document.write("<script language=javascript src='static/js/config.js'></script>");

$.ajaxSetup({
    cache: false //close AJAX cache
});

var app = new Vue({
    el: '#allActivities',
    data: {
        activitys: [],
        types: ['羽毛球', '篮球', '跑步', '游泳', '健身', '乒乓球', '足球', '网球', '冰雪', '其它'],
        cur_act: 1,
        is_su: false,
    },
    methods: {
        showActivityInfo: function(id) {
            console.log('/Details-activity.html?id=' + id);
            location.href = '/Details-activity.html?id=' + id;
        },
        deleteActivity: function(id) {
            if (confirm('确认删除吗？')) {
                $.ajax({
                    type: 'POST',
                    url: base_url + 'api/deleteActivity',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify({
                        activityId: id,
                    }),
                    dataType: 'json',
                    success: function(data) {
                        if (data['succeed']) {
                            alert('操作成功');
                        } else {
                            alert(data['errmsg']);
                        }
                        location.href = '/index.html'
                    }
                });
            }
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
});

function setTab(name, cursel, n) {
    app.cur_act = cursel;
    for (i = 1; i <= n; i++) {
        var menu = document.getElementById(name + i);
        if (menu) menu.className = ((i == cursel) ? "hover" : "");
    }
}
