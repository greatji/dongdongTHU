document.write('<script language=javascript src="/static/js/config.js"></script>');

$.ajaxSetup ({
    cache: false //close AJAX cache
});

$(document).ready(function() {
    $('#nav').load('/static/nav.html');
    vue_clubInfo = new Vue({
        el: '#submit_info',
        data: {
            club: {
                name: '',
                type: '',
                major: '',
                motto: '',
                remark: '',
                introduction: ''
            },
            try_submit: false,
        },
        methods: {
            submitClubInfo: function () {
                // console.log(this.club.name.length);
                // return true;
                this.try_submit = true;
                if (!this.canSubmit) return;
                $.ajax({
                    type: 'POST',
                    url: base_url + 'api/createClub',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify({
                        name: this.club.name,
                        type: this.club.type,
                        major: this.club.major,
                        motto: this.club.motto,
                        remark: this.club.remark,
                        introduction: this.club.introduction,
                        poster: ''
                    }),
                    dataType: 'json',
                    success: function (data) {
                        if (data['succeed']) {
                            alert('succeed');
                            location.href = '/club-list.html';
                        }  else {
                            if (data['errno'] === 2008) {
                                location.href = '/login.html';
                            } else {
                                alert('unknown error');
                                location.href = '/index.html';
                            }
                        }
                    }
                })
            }
        },
        computed: {
            name_ok: function() {
                return this.club.name.length >= 4 && this.club.name.length <= 16;
            },
            major_ok: function() {
                return !this.club.isForClub || this.club.filterMajors != [];
            },
            type_ok: function() {
                return this.club.type != '';
            },
            motto_ok: function() {
                return this.club.motto.length >= 4 && this.club.motto.length <= 16;
            },
            intro_ok: function() {
                return this.club.introduction.length >= 50 && this.club.introduction.length <= 200;
            },
            canSubmit: function() {
                // return true;
                return this.name_ok && this.major_ok && this.type_ok && this.motto_ok && this.intro_ok;
            },
        }
    })
    $.ajax({
        type: 'POST',
        url: base_url + 'api/getPersonalInfo',
        data: '{}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
            if (!data['succeed']) {
                if (data['errno'] === 2008) {
                    location.href = '/login.html';
                } else {
                    alert('unknown error');
                    location.href = '/index.html';
                }
            }
        }
    });
})
