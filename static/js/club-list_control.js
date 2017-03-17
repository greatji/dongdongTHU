/**
 * Created by hexiaohao on 2016/12/3.
 */

document.write("<script language=javascript src='static/js/config.js'></script>");

$.ajaxSetup ({
    cache: false //close AJAX cache
});

$(document).ready(function () {
    $('#nav').load('/static/nav.html');
    $.ajax({
        type: 'POST',
        url: base_url + 'api/listClubs',
        data: '{}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
            if (data['succeed']) {
                var clubList = new Vue({
                    el: '#clubList',
                    data: {
                        clubList: data['info']
                    },
                    methods: {
                        showClubInfo: function (event) {
                            location.href = '/Details-club.html?id=' + $(event.currentTarget).attr('id');
                        }
                    }
                });
            }
        }
    });
});