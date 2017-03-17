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
            canSubmit: false
        }, 
        methods: {
            submitClubInfo: function () {
                // console.log(this.club.name.length);
                // return true;
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
            canSubmit: function() {
                // return true;
                return this.club.name.length >= 4 && this.club.name.length <= 16 &&
                        this.club.type.length >= 2 && this.club.type.length <= 8 &&
                        this.club.major !== '' &&
                        this.club.motto.length >= 4 && this.club.motto.length <= 16 &&
                        this.club.introduction.length >= 50 && this.club.introduction.length <= 200;
            }
        }
    })
})