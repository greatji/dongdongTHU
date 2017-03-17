/**
 * Created by hexiaohao on 2016/12/2.
 */

document.write("<script language=javascript src='static/js/config.js'></script>");

$.ajaxSetup ({
    cache: false //close AJAX cache
});

$(document).ready(function () {
    $('#nav').load('/static/nav.html');
    $.ajax({
        type: 'POST',
        url: base_url + 'api/listActivities',
        data: '{}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
            if (data['succeed']) {
                console.log(data['info']);
                var activityList = new Vue({
                    el: '#activityList',
                    data: {
                        activityList: data['info']
                    },
                    methods: {
                        showActivityInfo: function () {
                            console.log('/Details-activity.html?id=' + $(event.currentTarget).attr('id'));
                            location.href = '/Details-activity.html?id=' + $(event.currentTarget).attr('id');
                        }
                    }
                });
            }
        }
    });
});