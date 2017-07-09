document.write('<script language=javascript src="/static/js/config.js"></script>');

$.ajaxSetup ({
    cache: false //close AJAX cache
});

$(document).ready(function () {
    $('#nav').load('/static/nav.html');
    vue_login = new Vue({
        el: '#login',
        data: {
            userid: '',
            passwd: '',
            error: false
        },
        methods: {
            submit_info: function () {
//                console.log(this.userid + ' ' + this.passwd);
                vue_login.error = false;
                var submitInfo = {
                    studentId: this.userid,
                    password: this.passwd
                };
                $.ajax({
                    type: 'POST',
                    url: base_url + 'api/login',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify(submitInfo),
                    dataType: 'json',
                    success: function(data) {
                        console.log(data);
                        if (data['succeed']) {
                            if (data['state'] === 1) {
                                location.href = '/setprofile.html';
                            } else if (data['state'] === 2 || data['state'] === 3) {
                                // console.log('登陆成功，会跳转到活动列表界面');
                                location.href = '/index.html';
                            }
                        } else {
                            vue_login.error = true;
                        }
                    }
                })
            }
        }
    })
})
