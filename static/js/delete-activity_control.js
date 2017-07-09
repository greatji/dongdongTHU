document.write("<script language=javascript src='static/js/config.js'></script>");

$.ajaxSetup ({
    cache: false //close AJAX cache
});

function param(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}

var activityId = param('id');

$(document).ready(function () {
    $('#nav').load('/static/nav.html');
    var activityDetails = new Vue({
        el: '#deleteActivity',
        data: {
            deleteReason: ''
        },
        methods: {
            deleteActivity: function() {
                $.ajax({
                    type: 'POST',
                    url: base_url + 'api/deleteActivity',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify({
                        activityId: activityId,
                        reason: this.deleteReason,
                        direct: true,
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
            },
        }
    });
});



