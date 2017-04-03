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
                introduction: '',
                isForClub: false,
                filterMajors: []
            },
            isAdmin: false,
            canSubmit: false,
            majors: [ '建筑学院', '土木系', '水利系', '环境学院', '机械系', '精仪系',
            '热能系', '汽车系', '工业工程系', '电机系', '电子系', '计算机系',
            '自动化系', '微纳电子系', '航天航空学院', '工物系', '化工系',
            '材料学院', '数学系', '物理系', '化学系', '生命学院', '地学中心',
            '交叉信息学院', '经管学院', '公管学院', '金融学院', '法学院',
            '新闻学院', '马克思主义学院', '人文学院', '社科学院', '美术学院',
            '核研院', '教研院', '医学院', '软件学院', '苏世民书院' ]
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
                    poster: '',
                    filterMajors: this.activity.filterMajors,
                    isForClub: this.activity.isForClub,
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
                                alert('unknown error');
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
        },
    });
    $.ajax({
        type: 'POST',
        url: base_url + 'api/getPersonalInfo',
        data: '{}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
            if (data.info.manager.length > 0) {
                vue_activityInfo.isAdmin = true;
            }
        }
    });
});
