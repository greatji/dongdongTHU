/**
 * Created by hexiaohao on 2016/11/30.
 */

document.write('<script language=javascript src="/static/js/config.js"></script>');

$.ajaxSetup ({
    cache: false //close AJAX cache
});

function param(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
}

var user_id = param('id');

$(document).ready(function () {
    $('#nav').load('/static/nav.html');
    // console.log(JSON.stringify({
    //     studentId: user_id
    // }))
    var submitData = (user_id === undefined || user_id === null)?{}:{studentId: user_id};
    console.log(submitData);
    $.ajax({
        type: 'POST',
        url:  base_url + 'api/getPersonalInfo',
        contentType: 'application/json; charset=utf-8',
        // data: '{"userId":"' + user_id + '"}',
        data: JSON.stringify(submitData),
        dataType: 'json',
        success: function (data) {
            console.log(data)
            if (data['succeed'] === false) {
                location.href = '/login.html';
                return
            }
            data = data['info'];
            user_info = new Vue({
                el: '#userInfo',
                data: {
                    user: data,
                },
                filters: {
                    lspace: function (x) {
                        var s = x.toString();
                        return Array(3 - s.length + 1).join('0') + s;
                        // return String.format('%03d', (x % 1000));
                    }
                },
                methods: {
                    modify_userInfo: function () {
                        $.ajax({
                            type: 'POST',
                            url: base_url + 'api/setPersonalInfo',
                            contentType: 'application/json; charset=utf-8',
                            // data: '{"userId":"' + user_id + '"}',
                            data: JSON.stringify({
                                userId: user_id
                            }),
                            dataType: 'json',
                            success: function (data) {
                                if (data['succeed']) {
                                    alert('succeed');
                                } else {
                                    if (data['errno'] === 2008) {
                                        location.href = '/login.html';
                                    } else {
                                        alert(data['errmsg']);
                                    }
                                }
                            }
                        })
                    }
                }
            });
        }
    });
});

// function hideBody() {
//     $('#userInfo').attr('hidden', 'hidden');
// }
