# coding=utf-8
errors = {
    'UNKNOWN_ERRNO': (999, '未知错误'),
    'JSON_PARSE': (1001, 'JSON数据解析失败'),
    'ARGUMENTS': (1002, '参数错误'),
    'VALIDATE_CODE_EXPIRED': (2001, 'Validate code expired'),
    'VALIDATE_CODE_WRONG': (2002, 'Validate code is wrong'),
    'USER_EXISTS': (2003, '用户名或邮箱已存在'),
    'USERNAME_PASSWORD_WRONG': (2005, '用户名或密码错误'),
    'NO_SUCH_USER': (2006, '该用户不存在'),
    'PASSWORD_WRONG': (2007, '密码错误'),
    'NOT_LOGGED_IN': (2008, '未登录'),
    'USER_INFORMATION_MODIFY_FAILED': (2009, '修改个人信息失败'),
    'CHECK ERROR': (3001, '无查询结果'),
    'PAGE OVERFLOW': (3002, 'Page is not valid'),
    'LABEL ERROR': (3003, 'some label checked is not included'),
    'NO_SUCH_CITY': (4001, 'city not found'),
    'NO_SUCH_ATTRACTION': (4002, 'attraction not found'),
    'NO_SUCH_COUNTRY': (4003, 'country not found'),
    'NO_IMG_UPLOADED': (5001, '无图片上传'),
    'NOT_VALID_IMAGE': (5002, '上传文件非图片'),
    'CLUB_NAME_EXISTS': (6001, '俱乐部名字已存在'),
    'CLUB_CREATE_FAILED': (6002, '创建俱乐部失败'),
    'CLUB_JOIN_FAILED': (6003, '加入俱乐部失败'),
    'CLUB_QUIT_FAILED': (6003, '退出俱乐部失败'),
    'CLUB_ID_EXISTS': (6004, '俱乐部ID已存在'),
    'HAS_NO_PRESIDENT': (6005, '您所在的院系尚无院系负责人'),
    'CLUB_INFORMATION_MODIFY_FAILED': (6006, '修改俱乐部信息失败'),
    'CLUB_NOT_EXIST': (6007, '该俱乐部不存在'),
    'ACTIVITY_JOIN_FAILED': (7001, '加入活动失败'),
    'COMMENT_FAILED': (7002, '评论失败'),
    'ACTIVITY_INFORMATION_MODIFY_FAILED': (7003, '修改活动信息失败'),
    'ACTIVITY_QUIT_FAILED': (7004, '退出失败'),
    'ACTIVITY_DELETE_FAILED': (7005, '删除失败'),
    'ACTIVITY_NOT_EXIST': (7006, '该活动不存在'),
    'ACTIVITY_FULL': (7007, '活动人数超出限制'),
    'ACTIVITY_MAJOR_NOT_MATCH': (7008, '本活动不对您所在的院系开放'),
    'ACTIVITY_THEME_BANNED': (7009, '活动主题不合要求'),
    'ACTIVITY_TOP_FAILED': (7010, '置顶失败'),
    'ACTIVITY_UNTOP_FAILED': (7010, '取消置顶失败'),
    'PERMISSION_DENIED': (9000, '无操作权限'),
    'SET_BANNED_WORDS_FAILED': (9001, '设置屏蔽词出错'),
}


def error(key, msg=None, remark=None):
    if key in errors:
        e = errors[key]
        if not msg:
            return {'succeed': False, 'errno': e[0], 'errmsg': e[1], 'remark': remark}
        else:
            return {'succeed': False, 'errno': e[0], 'errmsg': msg, 'remark': remark}
    else:
        if not msg:
            msg = "Unknown"
        return {'succeed': False, 'errno': None, 'errmsg': msg, 'remark': remark}


def success(**kwargs):
    res = {'succeed': True}
    if kwargs:
        res.update(kwargs)
    return res


def error_num(key):
    if key in errors:
        e = errors[key]
        return e[0]
    else:
        return errors['UNKNOWN_ERRNO'][0]
