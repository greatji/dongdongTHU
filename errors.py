# coding=utf-8
errors = {
    'UNKNOWN_ERRNO': (999, 'Unknown error number'),
    'JSON_PARSE': (1001, 'JSON parse error'),
    'ARGUMENTS': (1002, '参数错误'),
    'VALIDATE_CODE_EXPIRED': (2001, 'Validate code expired'),
    'VALIDATE_CODE_WRONG': (2002, 'Validate code is wrong'),
    'USER_EXISTS': (2003, 'Username or Email exists'),
    'USERNAME_PASSWORD_WRONG': (2005, 'Username or password is wrong'),
    'NO_SUCH_USER': (2006, 'No such user'),
    'PASSWORD_WRONG': (2007, 'Password is wrong'),
    'NOT_LOGGED_IN': (2008, 'Not logged in'),
    'USER_INFORMATION_MODIFY_FAILED': (2009, 'Failed to modify information'),
    'CHECK ERROR': (3001, 'No result fits qurey'),
    'PAGE OVERFLOW': (3002, 'Page is not valid'),
    'LABEL ERROR': (3003, 'some label checked is not included'),
    'NO_SUCH_CITY': (4001, 'city not found'),
    'NO_SUCH_ATTRACTION': (4002, 'attraction not found'),
    'NO_SUCH_COUNTRY': (4003, 'country not found'),
    'NO_IMG_UPLOADED': (5001, 'no image file is uploaded'),
    'NOT_VALID_IMAGE': (5002, 'the uploaded file is not image file'),
    'CLUB_NAME_EXISTS': (6001, 'Club name exists'),
    'CLUB_CREATE_FAILED': (6002, 'Failed to create club'),
    'CLUB_JOIN_FAILED': (6003, 'Failed to join club'),
    'CLUB_QUIT_FAILED': (6003, 'Failed to quit club'),
    'CLUB_ID_EXISTS': (6004, 'Club id exists'),
    'HAS_NO_PRESIDENT': (6005, '您所在的院系尚无院系负责人'),
    'CLUB_INFORMATION_MODIFY_FAILED': (6006, 'Failed to modify the information of club'),
    'CLUB_NOT_EXIST': (6007, 'The club does not exist'),
    'ACTIVITY_JOIN_FAILED': (7001, 'Failed to join this activity'),
    'COMMENT_FAILED': (7002, 'Failed to comment'),
    'ACTIVITY_INFORMATION_MODIFY_FAILED': (7003, 'Failed to modify the information of activity'),
    'ACTIVITY_QUIT_FAILED': (7004, 'Failed to quit activity'),
    'ACTIVITY_DELETE_FAILED': (7005, 'Failed to delete activity'),
    'ACTIVITY_NOT_EXIST': (7006, 'The activity does not exist'),
    'ACTIVITY_FULL': (7007, 'The activity is full'),
    'ACTIVITY_MAJOR_NOT_MATCH': (7008, '本活动不对您所在的院系开放'),
    'ACTIVITY_THEME_BANNED': (7009, '活动主题不合要求'),
    'PERMISSION_DENIED': (9000, 'Not authenticated to access this resource'),
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
