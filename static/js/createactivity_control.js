/**
 * Created by hexiaohao on 2016/12/4.
 */

document.write('<script language=javascript src="/static/js/config.js"></script>');

$.ajaxSetup ({
    cache: false //close AJAX cache
});

$(document).ready(function() {
    $('#nav').load('/static/nav.html');
    var vue_activityInfo = new Vue({
        el: '#submit_info',
        data: {
            activity: {
                name: '',
                startDate: '',
                starthour: '',
                startMinute: '',
                duration: '',
                type: '',
                address: '',
                capacity: '',
                introduction: ''
            },
            canSubmit: false,
        },
        methods: {
            submitActivityInfo: function () {
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
                    alert('时间有误，请您核对后重试');
                    return ;
                }
                var send_info = JSON.stringify({
                    name: this.activity.name,
                    address: this.activity.address,
                    capacity: parseInt(this.activity.capacity),
                    type: [this.activity.type],
                    introduction: this.activity.introduction,
                    duringTime: this.duringTime,
                    poster: ''
                });
                console.log(send_info);
                $.ajax({
                    type: 'POST',
                    url: base_url + 'api/activity/create',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify({
                        name: this.activity.name,
                        address: this.activity.address,
                        capacity: parseInt(this.activity.capacity),
                        type: [this.activity.type],
                        introduction: this.activity.introduction,
                        duringTime: this.duringTime,
                        poster: ''
                    }),
                    dataType: 'json',
                    success: function (data) {
                        if (data['succeed']) {
                            // alert('succeed');
                            location.href = '/activity-profile.html';
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
                return this.activity.name.length >= 4 && this.activity.name.length <= 12 &&
                    this.activity.startDate != '' &&
                    this.activity.address.length >= 2 && this.activity.address.length <= 10 &&
                    parseInt(this.activity.capacity) > 0 && parseInt(this.activity.capacity) <= 100 &&
                    this.activity.introduction.length <= 200;
            },
            duringTime: function () {
                var _date = this.activity.startDate.split('-');
                return {
                    year: parseInt(_date[0]),
                    month: parseInt(_date[1]),
                    day: parseInt(_date[2]),
                    shour: parseInt(this.activity.starthour),
                    sminute: parseInt(this.activity.startMinute),
                    hour: Math.floor(parseInt(this.activity.duration) / 60),
                    minute: parseInt(this.activity.duration) % 60
                }
            }
        }
    });
});
