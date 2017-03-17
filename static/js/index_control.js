/**
 * Created by hexiaohao on 2016/12/5.
 */

document.write("<script language=javascript src='static/js/config.js'></script>");

$.ajaxSetup ({
    cache: false //close AJAX cache
});

$(document).ready(function () {
    $('#nav').load('/static/nav.html');
    setTab('two',1,11);
    $.ajax({
        type: 'POST',
        url: base_url + 'api/listActivities',
        data: '{}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
            if (data['succeed']) {
                var allActivities = new Vue({
                    el: '#allActivities',
                    data: {
                        activitys: data['info']
                    },
                    computed: {
                        filterBadminton: function () {
                            return this.activitys.filter(function (activity) {
                                return activity['type'][0] === '羽毛球';
                            })
                        },
                        filterBasketball: function () {
                            return this.activitys.filter(function (activity) {
                                return activity['type'][0] === '篮球';
                            })
                        },
                        filterRun: function () {
                            return this.activitys.filter(function (activity) {
                                return activity['type'][0] === '跑步';
                            })
                        },
                        filterSwim: function () {
                            return this.activitys.filter(function (activity) {
                                return activity['type'][0] === '游泳';
                            })
                        },
                        filterGym: function () {
                            return this.activitys.filter(function (activity) {
                                return activity['type'][0] === '健身';
                            })
                        },
                        filterPingpong: function () {
                            return this.activitys.filter(function (activity) {
                                return activity['type'][0] === '乒乓球';
                            })
                        },
                        filterFootball: function () {
                            return this.activitys.filter(function (activity) {
                                return activity['type'][0] === '羽毛球';
                            })
                        },
                        filterTennis: function () {
                            return this.activitys.filter(function (activity) {
                                return activity['type'][0] === '网球';
                            })
                        },
                        filterSki: function () {
                            return this.activitys.filter(function (activity) {
                                return activity['type'][0] === '冰雪';
                            })
                        },
                        filterOther: function () {
                            return this.activitys.filter(function (activity) {
                                return activity['type'][0] === '其它';
                            })
                        },
                    },
                    methods: {
                        showActivityInfo: function () {
                            console.log('/Details-activity.html?id=' + $(event.currentTarget).attr('id'));
                            location.href = '/Details-activity.html?id=' + $(event.currentTarget).attr('id');
                        }
                    }
                });
            }
        }
    });
});
