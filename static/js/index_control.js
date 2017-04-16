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
        dissolveActivity: function(id) {
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
                            alert('succeed');
                        } else {
                            alert(data['errmsg']);
                        }
                        location.href = '/index.html'
                    }
                });
            }
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
                // alert('succeed');
                if (data.info.state == 3) {
                    app.is_su = true;
                }
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

var swiper = new Swiper('.swiper-container', {
    pagination: '.swiper-pagination',
    nextButton: '.swiper-button-next',
    prevButton: '.swiper-button-prev',
    slidesPerView: 1,
    paginationClickable: true,
    spaceBetween: 30,
    loop: true,
    autoplay: 3000,
    autoplayDisableOnInteraction: false
});
