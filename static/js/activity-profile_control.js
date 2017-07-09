document.write('<script language=javascript src="/static/js/config.js"></script>');

$.ajaxSetup({
    cache: false //close AJAX cache
});

function setTab(name,cursel,n){
 for(i=1;i<=n;i++){
  var menu=document.getElementById(name+i);
  var con=document.getElementById("con_"+name+"_"+i);
  if(menu) menu.className=((i==cursel)?"hover":"");
  if(con) con.style.display=((i==cursel)?"block":"none");
 }
}

$(document).ready(function () {
    $('#nav').load('/static/nav.html');
    vue_activity_profile = new Vue({
        el: '#activity_profile',
        data: {
            leadingActivities: [],
            jAct: []
        },
        methods: {
            leadingActivity: function () {
                setTab('one', 1, 2);
                $.ajax({
                    type: 'POST',
                    url: base_url + 'api/getActivityList',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify({
                        flag: 'manager'
                    }),
                    dataType: 'json',
                    success: function (data) {
                        if (data['succeed']) {
                            console.log(data['info']);
                            vue_activity_profile.leadingActivities = data['info'];
                            console.log(this);
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
            },
            joinedActivity: function () {
                setTab('one', 2, 2);
                $.ajax({
                    type: 'POST',
                    url: base_url + 'api/getActivityList',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify({
                        flag: 'member'
                    }),
                    dataType: 'json',
                    success: function (data) {
                        if (data['succeed']) {
                            vue_activity_profile.jAct = data['info'];
                            console.log(data['info']);
                            console.log(this.jAct);
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
            },
            toImageName: function(type) {
                switch (type) {
                    case "全部":
                        return "kind_all";
                    case "羽毛球":
                        return "kind_01";
                    case "篮球":
                        return "kind_02";
                    case "跑步":
                        return "kind_03";
                    case "游泳":
                        return "kind_04";
                    case "健身":
                        return "kind_05";
                    case "乒乓球":
                        return "kind_06";
                    case "足球":
                        return "kind_07";
                    case "网球":
                        return "kind_08";
                    case "冰雪":
                        return "kind_09";
                    case "其它":
                        return "kind_other";
                }
            }
        }
    });
    console.log(vue_activity_profile);
    $('#one1').trigger('click');
})
