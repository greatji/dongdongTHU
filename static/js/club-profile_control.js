document.write('<script language=javascript src="/static/js/config.js"></script>');

$.ajaxSetup({
    cache: false //close AJAX cache
});

var all_padding_size = 7;

function setTab(name,cursel,n){
 for(i=1;i<=n;i++){
  var menu=document.getElementById(name+i);
  var con=document.getElementById("con_"+name+"_"+i);
  if(menu) menu.className=((i==cursel)?"hover":"");
  if(con) con.style.display=((i==cursel)?"block":"none");
 }
}

function dealMyClubMethod() {
    setTab('one', 1, 3);
    $.ajax({
        type: 'POST',
        url: base_url + 'api/getClubList',
        contentType: 'application/json; charset=utf-8',
        // data: '{"userId":"' + user_id + '"}',
        data: JSON.stringify({
            flag: 'member'
        }),
        dataType: 'json',
        success: function (data) {
            if (data['succeed']) {
                vue_club_profile.myClubs = data['info'];
                console.log(data['info']);
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
}

function dealManagedClubMethod() {
    setTab('one', 2, 3);
    $.ajax({
        type: 'POST',
        url: base_url + 'api/getClubList',
        contentType: 'application/json; charset=utf-8',
        // data: '{"userId":"' + user_id + '"}',
        data: JSON.stringify({
            flag: 'manager'
        }),
        dataType: 'json',
        success: function (data) {
            if (data['succeed']) {
                vue_club_profile.managedClubs = data['info'];
                console.log(data['info']);
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
}

function dealPendingInfoMethod() {
    setTab('one', 3, 3);
    $.ajax({
        type: 'POST',
        url: base_url + 'api/getPendingInfo',
        contentType: 'application/json; charset=utf-8',
        // data: '{"userId":"' + user_id + '"}',
        data: JSON.stringify({}),
        dataType: 'json',
        success: function (data) {
            if (data['succeed']) {
                vue_club_profile.pendingInfos = data['info'];
                vue_club_profile.is_manager = true;
                data['info'].map(
                    function(info, index) {
                        console.log(info);
                        $.ajax({
                            type: 'POST',
                            url: base_url + 'api/getClub',
                            contentType: 'application/json; charset=utf-8',
                            data: '{"clubId":"' + info.info.clubId + '"}',
                            dataType: 'json',
                            success: function (data) {
                                if (data['succeed']) {
                                    info.detail = data['info'];
                                    $.ajax({
                                        type: 'POST',
                                        url:  base_url + 'api/getPersonalInfo',
                                        contentType: 'application/json; charset=utf-8',
                                        data: JSON.stringify({studentId: info.applyId, full:true}),
                                        dataType: 'json',
                                        success: function (data) {
                                            if (data['succeed']) {
                                                info.applyer = data['info'];
                                                vue_club_profile.pendingInfos.splice(index, 1, info);
                                                if (data['info']['state'] == 3) showAdmin();
                                            } else {
                                                alert(data['errmsg']);
                                                location.href = '/index.html';
                                            }
                                        }
                                    });
                                } else {
                                    alert(data['errmsg']);
                                    location.href = '/index.html';
                                }
                            }
                        });
                    }
                )
            } else {
                vue_club_profile.is_manager = false;
                if (data['errno'] === 2008) {
                    location.href = '/login.html';
                } else {
                    alert(data['errmsg']);
                    location.href = '/index.html';
                }
            }
        }
    })
}

function sendDeterminationMethod(id, determination) {
    $.ajax({
        type: 'POST',
        url: base_url + 'api/checkPendingInfo',
        contentType: 'application/json; charset=utf-8',
        // data: '{"userId":"' + user_id + '"}',
        data: JSON.stringify({
            pendingInfoId: id,
            flag: determination
        }),
        dataType: 'json',
        success: function (data) {
            if (data['succeed']) {
                var index = -1;
                for (i in vue_club_profile.pendingInfos) {
                    if (id === vue_club_profile.pendingInfos[i]['id']) {
                        index = i;
                        break;
                    }
                }
                console.log(index);
                if (index >= 0) {
                    vue_club_profile.pendingInfos.splice(index, 1);
                }
                // alert('succeed');
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
}

$(document).ready(function () {
    $('#nav').load('/static/nav.html');
    vue_club_profile = new Vue({
        el: '#vue_info',
        data: {
            pendingInfos: [],
            myClubs: [],
            managedClubs: [],
            is_manager: false,
        },
        methods: {
            dealPendingInfo: dealPendingInfoMethod,
            dealMyClub: dealMyClubMethod,
            sendDetermination: sendDeterminationMethod,
            dealManagedClub: dealManagedClubMethod,
            showActivityInfo: function () {
                location.href = '/Details-activity.html?id=' + $(event.currentTarget).attr('id');
            },
            toChinese: function (x) {
                switch (x) {
                    case 'delete':
                        return '被管理员删除';
                    case 'refuse':
                        return '申请失败';
                    case 'pending':
                        return '审核中';
                    case 'admit':
                        return '申请成功';
                    default:
                        return '';
                }
            },
            toChinese2: function (x) {
                switch (x) {
                    case 'deleteClub':
                        return '删除';
                    case 'joinClub':
                        return '加入';
                    case 'createClub':
                        return '创建';
                    default:
                        return '';
                }
            }
        },
        beforeCreate: function () {
            dealPendingInfoMethod();
            dealMyClubMethod();
        }
    })
    // $('body').css('background', 'radial-gradient(#8b4a75,#4b2a4f)');
})
