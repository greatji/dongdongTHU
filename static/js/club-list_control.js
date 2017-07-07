/**
 * Created by hexiaohao on 2016/12/3.
 */

document.write("<script language=javascript src='static/js/config.js'></script>");

$.ajaxSetup ({
    cache: false //close AJAX cache
});

var app = new Vue({
    el: '#clubList',
    data: {
        clubList: [],
        types: ['羽毛球', '篮球', '跑步', '游泳', '健身', '乒乓球', '足球', '网球', '冰雪', '其它'],
        cur_club: 1
    },
    methods: {
        showClubInfo: function (event) {
            location.href = '/Details-club.html?id=' + $(event.currentTarget).attr('id');
        }
    }
});

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
        url: base_url + 'api/listClubs',
        data: '{}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
            if (data['succeed']) {
                app.clubList = data['info'];
            }
        }
    });
});

function setTab(name, cursel, n) {
    app.cur_club = cursel;
    for (i = 1; i <= n; i++) {
        var menu = document.getElementById(name + i);
        if (menu) menu.className = ((i == cursel) ? "hover" : "");
    }
}

