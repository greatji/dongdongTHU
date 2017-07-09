/**
 * Created by hexiaohao on 2016/12/4.
 */

document.write('<script language=javascript src="/static/js/config.js"></script>');

$.ajaxSetup ({
    cache: false //close AJAX cache
});

$(document).ready(function() {
    $('#nav').load('/static/nav.html');
	//$('#multiplemajor').multipleSelect();
    vue_activityInfo = new Vue({
        el: '#submit_info',
        data: {
            activity: {
                name: '',
                startDate: '',
                startTime: '',
                duration: '',
                type: '',
                address: '',
                capacity: '',
                introduction: '',
                isForClub: false,
                filterMajors: []
            },
            try_submit: false,
            time_ok: false,
            isAdmin: false,
        },
        methods: {
            submitActivityInfo: function () {
                this.try_submit = true;
                var now_date = new Date().getTime();
                var input_date = new Date();
                console.log(vue_activityInfo.duringTime);
                console.log(new Date());
                input_date.setFullYear(vue_activityInfo.duringTime.year);
                input_date.setMonth(vue_activityInfo.duringTime.month - 1); // [0,11]
                input_date.setDate(vue_activityInfo.duringTime.day);
                input_date.setHours(vue_activityInfo.duringTime.shour);
                input_date.setMinutes(vue_activityInfo.duringTime.sminute);
                console.log(input_date);
                input_date = input_date.getTime();
                console.log(now_date);
                console.log(input_date);
                if (now_date + 1000 * 60 * 30 >= input_date) {
                    this.time_ok = false;
                    return;
                }
                this.time_ok = true;
                if (!this.canSubmit) return;
                var send_info = JSON.stringify({
                    name: this.activity.name,
                    address: this.activity.address,
                    capacity: parseInt(this.activity.capacity),
                    type: [this.activity.type],
                    introduction: this.activity.introduction,
                    duringTime: this.duringTime,
                    poster: '',
                    remark: '',
                    filterMajors: this.activity.isForClub ? this.activity.filterMajors : [],
                });
                console.log(send_info);
                $.ajax({
                    type: 'POST',
                    url: base_url + 'api/activity/create',
                    contentType: 'application/json; charset=utf-8',
                    data: send_info,
                    dataType: 'json',
                    success: function (data) {
                        if (data['succeed']) {
                            // alert('succeed');
                            location.href = '/activity-profile.html';
                        }  else {
                            if (data['errno'] === 2008) {
                                location.href = '/login.html';
                            } else {
                                alert(data['errmsg']);
                                location.href = '/index.html';
                            }
                        }
                    }
                })
            },
            updateSelected: function (newSelected) {
              this.activity.filterMajors = newSelected
            },
        },
        computed: {
            name_ok: function() {
                return this.activity.name.length >= 4 && this.activity.name.length <= 12;
            },
            date_ok: function() {
                return this.activity.startDate != '';
            },
            major_ok: function() {
                return !this.activity.isForClub || this.activity.filterMajors != [];
            },
            duration_ok: function() {
                return this.activity.duration != '';
            },
            type_ok: function() {
                return this.activity.type != '';
            },
            address_ok: function() {
                return this.activity.address.length >= 2 && this.activity.address.length <= 10;
            },
            capacity_ok: function() {
                return parseInt(this.activity.capacity) > 0 && parseInt(this.activity.capacity) <= 100;
            },
            intro_ok: function() {
                return this.activity.introduction.length <= 200;
            },
            canSubmit: function() {
                // return true;
                return this.name_ok && this.date_ok && this.time_ok && this.major_ok && this.duration_ok
                    && this.type_ok && this.address_ok && this.capacity_ok && this.intro_ok;
            },
            duringTime: function () {
                var _date = this.activity.startDate.split('-');
                var _time = this.activity.startTime.split(':');
                return {
                    year: parseInt(_date[0]),
                    month: parseInt(_date[1]),
                    day: parseInt(_date[2]),
                    shour: parseInt(_time[0]),
                    sminute: parseInt(_time[1]),
                    hour: Math.floor(parseInt(this.activity.duration) / 60),
                    minute: parseInt(this.activity.duration) % 60
                }
            }
        },
    });
    $.ajax({
        type: 'POST',
        url: base_url + 'api/getPersonalInfo',
        data: '{}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
            if (data['succeed']) {
                // alert('succeed');
                if (data.info.manager.length > 0) {
                    vue_activityInfo.isAdmin = true;
                }
            }  else {
                if (data['errno'] === 2008) {
                    location.href = '/login.html';
                } else {
                    alert(data['errmsg']);
                    location.href = '/index.html';
                }
            }
        }
    });
});

