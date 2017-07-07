/**
 * Created by hexiaohao on 2016/12/3.
 */

document.write("<script language=javascript src='static/js/config.js'></script>");

$.ajaxSetup ({
    cache: false //close AJAX cache
});

var app = new Vue({
    el: '#manage_club',
    data: {
        clubList: [],
        filter_major: '',
        filter_type: '',
    },
    methods: {
        searchClub: function () {
            if (this.filter_major == '' && this.filter_type == '') {
                alert('请至少提供一项筛选');
            }
            $.ajax({
                type: 'POST',
                url: base_url + 'api/searchClub',
                //data: '{' + (this.filter_major == '' ? ('"major":"'+this.filter_major+'",') : '') + (this.filter_type == '' ? ('"major":"'+this.filter_type+'",') : '') '}',
                data: JSON.stringify({
                    major: this.filter_major == '' ? undefined : this.filter_major,
                    type: this.filter_type == '' ? undefined : this.filter_type,
                }),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                success: function (data) {
                    if (data['succeed']) {
                        app.clubList = data['info'];
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

