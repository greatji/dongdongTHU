/**
 * Created by hexiaohao on 2016/12/3.
 */

document.write("<script language=javascript src='static/js/config.js'></script>");

$.ajaxSetup ({
    cache: false //close AJAX cache
});

var app = new Vue({
    el: '#manage_user',
    data: {
        userList: [],
        filter_id: '',
        filter_name: '',
    },
    methods: {
        showUserInfo: function (id) {
            location.href = '/manage-user-detail.html?id=' + id;
        },
        searchUser: function () {
            if (this.filter_id == '' && this.filter_name == '') {
                alert('请至少提供一项筛选');
                return;
            }
            $.ajax({
                type: 'POST',
                url: base_url + 'api/searchUser',
                //data: '{' + (this.filter_major == '' ? ('"major":"'+this.filter_major+'",') : '') + (this.filter_type == '' ? ('"major":"'+this.filter_type+'",') : '') '}',
                data: JSON.stringify({
                    studentId: this.filter_id == '' ? undefined : this.filter_id,
                    studentName: this.filter_name == '' ? undefined : this.filter_name,
                }),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                success: function (data) {
                    if (data['succeed']) {
                        app.userList = data['info'];
                    } else {
                        alert(data['errmsg']);
                    }
                }
            });

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
});


