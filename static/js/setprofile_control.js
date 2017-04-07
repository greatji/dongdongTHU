document.write('<script language=javascript src="/static/js/config.js"></script>');

function is_email(s) {

}

$.ajaxSetup({
    cache: false //close AJAX cache
});

$(document).ready(function () {
    $('#nav').load('/static/nav.html');
    $.ajax({
        // /api/getPersonalInfo
        type: 'POST',
        url: base_url + 'api/getPersonalInfo',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({}),
        dataType: 'json',
        success: function (data) {
            console.log(data);
            if (data['succeed']) {
                vue_profile = new Vue({
                    el: '#profile',
                    data: {
                        user: data['info'],
                        try_submit: false,
                    },
                    computed: {
                        sex_error: function() {
                            return this.user.sex !== '男' && this.user.sex !== '女';
                        },
                        phone_error: function () {
                            // console.log(this.user.phone.length);
                            return this.user.phone.length !== 11 || parseInt(this.user.phone, 10) === NaN;
                        },
                        email_error: function () {
                            return this.user.email.length < 5 || this.user.email.length > 128 || this.user.email.indexOf('@') < 0;
                        },
                        tag_error: function () {
                            return this.user.tag.length > 12 || this.user.tag.length < 2;
                        },
                        introduction_error: function () {
                            return this.user.introduction.length > 12 || this.user.introduction.length < 4;
                        },
                        all_right: function () {
                            return this.user.sex !== "" && this.user.major !== "" && (!this.sex_error) && (!this.phone_error) && (!this.email_error) && (!this.tag_error) && (!this.introduction_error);
                        }
                    },
                    methods: {
                        submitInfo: function () {
                            this.try_submit = true;
                            if (!this.all_right) return;
                            submitInfo = {
                                email: this.user.email,
                                phone: this.user.phone,
                                major: this.user.major,
                                sex: this.user.sex,
                                tag: this.user.tag,
                                introduction: this.user.introduction,
                                selfPhoto: ''
                            }
                            console.log(submitInfo);
                            $.ajax({
                                type: 'POST',
                                url: base_url + 'api/setPersonalInfo',
                                contentType: 'application/json; charset=utf-8',
                                data: JSON.stringify(submitInfo),
                                dataType: 'json',
                                success: function (data) {
                                    if (data['succeed']) {
                                        // console.log('成功');
                                        location.href = '/index.html';
                                    } else {
                                        alert(data['errmsg']);
                                    }
                                }
                            })
                        }
                    }
                })
            } else {
                if (data['errno'] === 2008) {
                    location.href = '/login.html';
                } else {
                    alert(data['errmsg']);
                    location.href = '/index.html';
                }
            }
        }
    })
})
