from appConfig import app, initialize
from flask import request, render_template, session, redirect
import flask
from utils import jsonApi, checkSensitiveWords, addRefreshStateList, popRefreshStateList
from checkers import *
from club import *
from activity import *
from pendInfo import *
from user import *
from parameter import *
from errors import error, success
from login import *
from loginAPI import *

# @app.route('/index', methods = ['GET'])
# def hello():
#     return render_template('index.html')
#
# ### activity
#
# #### page
#
# @app.route('/activities', methods = ['GET'])
# def listActivities():
#     return render_template('index.html')
#     pass
#
# @app.route('/activity', methods = ['GET'])
# def getActivity():
#     pass
#
# @app.route('/clubs', methods = ['GET'])
# def listClubs():
#     pass
#
# @app.route('/club', methods = ['GET'])
# def getClub():
#     pass

# API

# login logout

import hashlib


@app.route('/weixin', methods=['GET'])
def weixin():
    # TOKEN = 'PEplatform'
    # signature = request.args.get('signature')
    # timestamp = request.args.get('timestamp')
    # nonce     = request.args.get('nonce')
    echostr = request.args.get('echostr')
    # if signature and timestamp and nonce and echostr:
    #    arr = [TOKEN, timestamp, nonce]
    #    sorted(arr)
    #    arr2 = ''.join(arr)
    #    a = hashlib.sha1(arr2)
    #    if a == signature:
    #        return echostr
    #    else:
    #        return 'ERR'
    # else:
    #    return 'ERR'
    return echostr


@app.route('/api/login', methods=['POST'])
@jsonApi(
    studentId=allChecked(lenIn(10, 10), isAllDigits),
    password=isStr
)
def apiLogin(studentId, password):
    session.permanent = True
    myLoginHelper = loginAndGetName()
    flag, name = myLoginHelper(studentId, password)
    if flag:
        res = createPersonalInfoService(studentId, name)
        if res == 0:
            return error('USERNAME_PASSWORD_WRONG')
        else:
            session['studentId'] = studentId
            session['studentName'] = name
            session['state'] = res
            return success(state=session['state'])
    else:
        return error('USERNAME_PASSWORD_WRONG')


def apiCheckSession(state=2):
    if all(['studentId' in session, 'state' in session]):
        needFresh = popRefreshStateList(session['studentId'])
        if needFresh:
            userInfo = getPersonalInfoService(session['studentId'])
            if not isinstance(userInfo, basestring):
                session['state'] = userInfo['state']
        if session['state'] >= state:
            return True
    return False


@app.route('/api/logout', methods=['POST'])
@jsonApi(
)
def apiLogout():
    if 'studentId' in session:
        del session['studentName'], session['studentId'], session['state']
    return success()


@app.route('/api/iflogin', methods=['POST'])
@jsonApi(
)
def apiIfLogin():
    if 'studentId' in session:
        return success(res=True)
    else:
        return success(res=False)


# activity


@app.route('/api/listActivities', methods=['POST'])
@jsonApi(
    skip=optional(isPositive),
    limit=optional(isPositive),
)
def apiListActivities(skip=0, limit=200):
    if apiCheckSession():
        info = getPersonalInfoService(session['studentId'])
        major = info['major']
    else:
        major = ''

    res = listActivitiesService(skip, limit, {
        'state': 'open',
        '$or': [{'filterMajors': {'$exists': False}}, {'filterMajors': major}]
    })
    return error('CHECK ERROR') if res is None else success(info=res)


@app.route('/api/getActivityList', methods=['POST'])
@jsonApi(
    skip=optional(isPositive),
    limit=optional(isPositive),
    flag=checkFlag,
)
def apiGetActivityList(flag, skip=0, limit=200):
    if apiCheckSession():
        if flag == 'member':
            res = listActivitiesService(skip, limit, {'$or': [{'participants.id': session['studentId']},
                                                              {'leader.id': session['studentId']}]})
            # res1 = listActivitiesService(skip, limit, {'$or': {'participants.id': session['studentId'], }})
            # res2 = listActivitiesService(skip, limit, {'leader.id': session['studentId']})
            # res = res1 + res2
            # print len(res), len(res1), len(res2)
            return success(info=res)
        elif flag == 'manager':
            res = listActivitiesService(skip, limit, {'leader.id': session['studentId']})
            return success(info=res)
        else:
            return error('CHECK ERROR')
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/getActivity', methods=['POST'])
@jsonApi(
    activityId=allChecked(lenIn(5, 5), isAllDigits)
)
def apiGetActivity(activityId):
    res = getActivityService(activityId)
    if res is None:
        return error('ACTIVITY_NOT_EXIST')
    if apiCheckSession():
        isParticipant = searchParticipant(activityId, session['studentId'])
        isOrganizer = searchOrganizer(activityId, session['studentId'])
        if isParticipant or isOrganizer:
            if isOrganizer:
                res['identity'] = 'organizer'
            else:
                res['identity'] = 'participant'
        else:
            res['identity'] = 'non-participant'
            filterSensitiveInfo(res['participants'])
    else:
        res['identity'] = 'nobody'
        filterSensitiveInfo(res['participants'])
    return success(info=res)


@app.route('/api/activity/create', methods=['POST'])
@jsonApi(
    name=lenIn(4, 12),
    duringTime=checkDuringTime,
    address=lenIn(2, 10),
    capacity=checkCapacity,
    type=checkType,
    introduction=lenIn(0, 200),
    poster=isStr,
    filterMajors=optional(checkMajorList),
)
def apiCreateActivity(name, duringTime, address, capacity, type, introduction, poster, filterMajors=None):
    if apiCheckSession():
        leader = traitAttr(getPersonalInfoService(session['studentId']), {
            'id': session['studentId'], 'name': session['studentName'], 'phone': '', 'major': '', 'selfPhoto': '',
            'introduction': ''
        })
        if filterMajors:
            if not isManager(session['studentId']):
                return error('PERMISSION_DENIED')
        if not checkSensitiveWords(name):
            return error('ACTIVITY_THEME_BANNED')
        res = createActivityService(name, duringTime, address, capacity, type, introduction, leader, poster,
                                    filterMajors)
        if res:
            updateTimes(session['studentId'], 1)
            return success()
        else:
            return error('CHECK ERROR')
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/activity/set', methods=['POST'])
@jsonApi(
    activityId=allChecked(lenIn(5, 5), isAllDigits),
    name=lenIn(4, 12),
    duringTime=checkDuringTime,
    address=lenIn(2, 10),
    capacity=isPositive,
    type=checkType,
    introduction=lenIn(50, 200)
)
def apiSetActivityInfo(activityId, name, duringTime, address, capacity, type, introduction):
    if apiCheckSession():
        res = updateActivityInfoService(activityId, session['studentId'], session['studentName'],
                                        name, duringTime, address, capacity, type, introduction)
        print res
        if isStr(res):
            return error(res)
        else:
            return success()
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/activity/addParticipant', methods=['POST'])
@jsonApi(
    activityId=allChecked(lenIn(5, 5), isAllDigits)
)
def apiAddParticipant(activityId):
    if apiCheckSession():
        participant = traitAttr(getPersonalInfoService(session['studentId']), {
            'id': session['studentId'], 'name': session['studentName'], 'phone': '', 'major': '', 'selfPhoto': '',
            'introduction': ''
        })
        # print participant
        res = addParticipant(activityId, participant)
        if res is None:
            return error('ACTIVITY_JOIN_FAILED')
        elif res is False:
            return error('ACTIVITY_NOT_EXIST')
        elif res == error_num('ACTIVITY_FULL'):
            return error('ACTIVITY_FULL')
        elif res == error_num('ACTIVITY_MAJOR_NOT_MATCH'):
            return error('ACTIVITY_MAJOR_NOT_MATCH')
        else:
            updateTimes(session['studentId'], 1)
            return success(info=res)
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/deleteActivity', methods=['POST'])
@jsonApi(
    activityId=allChecked(lenIn(5, 5), isAllDigits)
)
def apiDeleteActivity(activityId):
    if apiCheckSession():
        isOrganizer = searchOrganizer(activityId, session['studentId'])
        isSuperuser = apiCheckSession(3)
        # print 'isSuper', isSuperuser, session['state']
        if isOrganizer or isSuperuser:
            res = deleteActivityService(activityId)
            if res:
                return success()
            else:
                return error('ACTIVITY_DELETE_FAILED')
        else:
            return error('PERMISSION_DENIED')
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/quitActivity', methods=['POST'])
@jsonApi(
    activityId=allChecked(lenIn(5, 5), isAllDigits)
)
def apiQuitActivity(activityId):
    if apiCheckSession():
        isParticipant = searchParticipant(activityId, session['studentId'])
        if isParticipant:
            res = quitActivityService(activityId, session['studentId'])
            if res:
                updateTimes(session['studentId'], -1)
                return success()
            else:
                return error('ACTIVITY_QUIT_FAILED')
        return error('ACTIVITY_QUIT_FAILED')
    else:
        return error('NOT_LOGGED_IN')


### comment operation
@app.route('/api/activity/getComment', methods=['POST'])
@jsonApi(
    activityId=allChecked(lenIn(5, 5), isAllDigits),
)
def apiGetComment(activityId):
    if apiCheckSession():
        isOrganizer = searchOrganizer(activityId, session['studentId'])
        if isOrganizer or searchParticipant(activityId, session['studentId']):
            res = getActivityService(activityId)
            if res is None:
                return error('ACTIVITY_NOT_EXIST')
            return success(info=res.get('comments', []))
        else:
            return error('PERMISSION_DENIED')
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/activity/addComment', methods=['POST'])
@jsonApi(
    activityId=allChecked(lenIn(5, 5), isAllDigits),
    content=isStr
)
def apiAddComment(activityId, content):
    if apiCheckSession():
        isOrganizer = searchOrganizer(activityId, session['studentId'])
        if isOrganizer or searchParticipant(activityId, session['studentId']):
            res = addComment(session['studentId'], session['studentName'], activityId, content)
            if isStr(res):
                return error(res)
            else:
                return success(info=res)
        else:
            return error('PERMISSION_DENIED')
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/activity/top', methods=['POST'])
@jsonApi(
    activityId=allChecked(lenIn(5, 5), isAllDigits),
    top=isBool,
)
def apiTopActivity(activityId, top):
    if apiCheckSession(3):
        res = topActivityService(activityId, top)
        if not res:
            errorType = 'ACTIVITY_TOP_FAILED' if top else 'ACTIVITY_UNTOP_FAILED'
            return error(errorType)
        else:
            success()
    else:
        return error('PERMISSION_DENIED')

# club

"""
Clubs List
"""


@app.route('/api/listClubs', methods=['POST'])
@jsonApi(
    skip=optional(isPositive),
    limit=optional(isPositive)
)
def apiListClubs(skip=0, limit=200):
    res = listClubsService(skip, limit, {'state': 'admit'})
    return success(info=res)


"""
Club detail
"""


@app.route('/api/getClub', methods=['POST'])
@jsonApi(
    clubId=allChecked(lenIn(9, 9), isAllDigits)
)
def apiGetClub(clubId):
    res = getClubService(clubId, ['joined'])
    if isStr(res):
        return error(res)
    if apiCheckSession():
        isMember = searchMember(clubId, session['studentId'])
        if isMember:
            isLeader = searchLeader(clubId, session['studentId'])
            if isLeader:
                res['identity'] = 'leader'
            else:
                res['identity'] = 'member'
        else:
            res['identity'] = 'non-member'

    else:
        res['identity'] = 'nobody'
    if res['state'] == 'pending':
        if apiCheckSession():
            permissionPeople = [person['id'] for person in getPresidentOfMajor(res['major'])]
            permissionPeople.append(res['leader']['id'])
            print permissionPeople
            if session['studentId'] not in permissionPeople:
                return error('PERMISSION_DENIED')
        else:
            return error('NOT_LOGGED_IN')
    return success(info=res)


"""
My Clublist
"""


@app.route('/api/getClubList', methods=['POST'])
@jsonApi(
    skip=optional(isPositive),
    limit=optional(isPositive),
    flag=checkFlag,
)
def apiGetClubList(flag, skip=0, limit=200):
    if apiCheckSession():
        if flag == 'member':
            res = listClubsService(skip, limit, {'state': 'admit', 'members': {
                '$elemMatch': {'id': session['studentId'], 'state': 'joined'}}})
            # 'members.id': session['studentId'],
            # 'members.state': 'joined'})
            # print res
            return success(info=res)
        elif flag == 'manager':
            res = listClubsService(skip, limit, {'managers.id': session['studentId']})
            return success(info=res)
        else:
            return error('CHECK ERROR')
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/searchClub', methods=['GET'])
@jsonApi(
    skip=optional(isPositive),
    limit=optional(isPositive),
    major=optional(checkMajor),
    type=optional(lenIn(2, 8)),
)
def apiSearchClub(skip=0, limit=0, major=None, type=None):
    if apiCheckSession(3):
        para = {}
        if major:
            para['major'] = major
        if type:
            para['type'] = type
        if not para:
            error('ARGUMENTS')
        para['state'] = 'admit'
        res = listClubsService(skip, limit, para)
        return success(info=res)

    else:
        return error('PERMISSION_DENIED')


@app.route('/api/createClub', methods=['POST'])
@jsonApi(
    # clubId=allChecked(lenIn(9, 9), isAllDigits),
    name=lenIn(4, 16),
    type=lenIn(2, 8),
    major=checkMajor,
    motto=isStr,
    remark=isStr,
    introduction=isStr,
    poster=isStr,
)
def apiCreateClub(name, type, major, motto, remark, introduction, poster):
    if apiCheckSession():
        leader = {'id': session['studentId'], 'name': session['studentName']}
        manager = {'id': session['studentId'], 'name': session['studentName']}
        member = traitAttr(getPersonalInfoService(session['studentId']), {
            'id': session['studentId'], 'name': session['studentName'], 'phone': '', 'major': '', 'introduction': '',
            'selfPhoto': ''
        })
        member['state'] = 'joined'
        res = getPresidentOfMajor(major)
        president = []
        if len(res) == 0:
            return error('HAS_NO_PRESIDENT')
        else:
            for i in res:
                president.append(i['id'])
        clubId = str(int(datetime.datetime.now().year)) + major_type[major] + str(int(getAndUpdateClubId(major))).zfill(
            3)
        res = createClubService(clubId, name, type, major, motto, remark, introduction, poster, leader, manager, member)
        if res == 0:
            return error('CLUB_CREATE_FAILED')
        elif res == 1:
            res_pendingInfo = createPendingInfo(
                applyId=session['studentId'],
                applyName=session['studentName'],
                checkId=president,
                type='createClub',
                info={
                    'clubId': clubId,
                    'clubName': name,
                    'major': major
                }
            )
            if not res_pendingInfo:
                return error('CLUB_CREATE_FAILED')
            else:
                return success()
        elif res == 2:
            return error('CLUB_NAME_EXISTS')
        elif res == 3:
            return error('CLUB_ID_EXISTS')
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/setClubInfo', methods=['POST'])
@jsonApi(
    clubId=allChecked(lenIn(9, 9), isAllDigits),
    name=lenIn(4, 16),
    type=checkType,
    introduction=isStr,
    major=checkMajor
)
def apiSetClubInfo(clubId, name, type, introduction, major):
    if apiCheckSession():
        res = updateClubInfoService(session['studentId'], session['studentName'],
                                    clubId, name, type, introduction, major)
        if isStr(res):
            return error(res)
        else:
            return success()
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/deleteClub', methods=['POST'])
@jsonApi(
    clubId=allChecked(lenIn(9, 9), isAllDigits),
    direct=optional(isBool),
    reason=optional(lenIn(0, 100)),
)
def apiDeleteClub(clubId, direct=False, reason=""):
    if apiCheckSession():
        if direct:  # super user or major president direct delete
            major = getMajor(clubId)
            if major is None:
                return error('PERMISSION_DENIED')
            presidents = getPresidentOfMajor(major)
            if apiCheckSession(3) or session['studentId'] in presidents:
                res = changeClubState(clubId, 'delete', reason) and delManagerService(clubId, '', session['studentId'])
                if not res:
                    return error('CHECK ERROR')
                else:
                    return success()
            else:
                return error('PERMISSION_DENIED')
        isLeader = searchLeader(clubId, session['studentId'])
        if isLeader:
            res_club = getClubService(clubId, ['joined'])
            if isStr(res_club):
                return error(res_club)
            res_president = getPresidentOfMajor(res_club['major'])
            president = []
            if len(res_president) == 0:
                return error('HAS_NO_PRESIDENT')
            else:
                for i in res_president:
                    president.append(i['id'])
            res_pendingInfo = createPendingInfo(
                applyId=session['studentId'],
                applyName=session['studentName'],
                checkId=president,
                type='deleteClub',
                info={
                    'clubId': clubId,
                    'clubName': res_club['name'],
                    'major': res_club['major']
                }
            )
            if not res_pendingInfo:
                return error('CLUB_CREATE_FAILED')
            else:
                return success()
        else:
            return error('PERMISSION_DENIED')
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/quitClub', methods=['POST'])
@jsonApi(
    clubId=allChecked(lenIn(9, 9), isAllDigits)
)
def apiQuitClub(clubId):
    if apiCheckSession():
        isMember = searchMember(clubId, session['studentId'])
        isLeader = searchLeader(clubId, session['studentId'])
        if isMember and (not isLeader):
            res = quitClubService(clubId, session['studentId'])
            if res:
                return success()
            else:
                return error('CLUB_QUIT_FAILED')
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/joinClub', methods=['POST'])
@jsonApi(
    clubId=allChecked(lenIn(9, 9), isAllDigits)
)
def apiJoinClub(clubId):
    if apiCheckSession():
        member = traitAttr(getPersonalInfoService(session['studentId']), {
            'id': session['studentId'], 'name': session['studentName'], 'phone': '', 'major': '', 'introduction': '',
            'selfPhoto': ''
        })
        member['state'] = 'apply'
        res = joinClubService(clubId, member)
        if res is None:
            return error('CLUB_JOIN_FAILED')
        elif res is False:
            return error('CHECK ERROR')
        else:
            manager = []
            for i in res['managers']:
                manager.append(i['id'])
            res = createPendingInfo(
                applyId=session['studentId'],
                applyName=session['studentName'],
                checkId=manager,
                type='joinClub',
                info={
                    'clubId': res['id'],
                    'clubName': res['name'],
                    'major': res['major']
                }
            )
            if res:
                return success()
            else:
                return error('CLUB_JOIN_FAILED')

    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/admitJoinClub', methods=['POST'])
@jsonApi(
    cludId=allChecked(lenIn(9, 9), isAllDigits),
    memberId=allChecked(lenIn(10, 10), isAllDigits)
)
def apiAdmitJoinClub(clubId, memberId):
    return apiChangeMemberState(clubId, memberId, 'joined')


def apiChangeMemberState(clubId, memberId, state):
    if apiCheckSession():
        res = changeMemberState(clubId, session['studentId'], memberId, state)
        if res is None:
            return error('CHECK ERROR')
        elif res:
            return success()
        else:
            return error('CHECK ERROR')
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/changeClubLeader', methods=['POST'])
@jsonApi(
    cludId=allChecked(lenIn(9, 9), isAllDigits),
    leaderId=allChecked(lenIn(10, 10), isAllDigits),
    leaderName=isStr,
)
def apichangeClubLeader(clubId, leaderId, leaderName):
    if apiCheckSession():
        canOperate = apiCheckSession(3)
        if not canOperate:
            major = getMajor(clubId)
            if not major:
                return error('CHECK_ERROR')
            presidents = getPresidentOfMajor(major)
            if session['studentId'] in presidents:
                canOperate = True
        if not canOperate:
            return error('PERMISSION_DENIED')
        userInfo = getPersonalInfoService(leaderId)
        if isStr(userInfo):
            return error(userInfo)
        if userInfo['name'] != leaderName:
            return error('NO_SUCH_USER')
        res = changeClubLeaderService(clubId, leaderId, leaderName)
        if not res:
            return error("CHECK_ERROR")
        else:
            return success()
    else:
        return error('PERMISSION_DENIED')


# pending


@app.route('/api/checkPendingInfo', methods=['POST'])
@jsonApi(
    pendingInfoId=allChecked(lenIn(15, 15), isAllDigits),
    flag=isBool
)
def checkPendingInfo(pendingInfoId, flag):
    if apiCheckSession():
        res = getPendingInfoByPendingInfoId(pendingInfoId, session['studentId'])
        if res is None:
            return error('CHECK ERROR')
        else:

            def dealWithPendingInfo(innerRes, infoType, flag):
                print innerRes
                if infoType == 'createClub':
                    state = 'admit' if flag else 'refuse'
                    isSuccess = (changeClubState(innerRes['info']['clubId'], state)
                                 and addManagerService(innerRes['info']['clubId'], innerRes['info']['clubName'],
                                                       innerRes['applyId'], state))
                    return isSuccess
                elif infoType == 'deleteClub':
                    if flag:
                        return (deleteClubService(innerRes['info']['clubId'])
                                and deletePendingInfoByClubId(innerRes['info']['clubId'])
                                and delManagerService(innerRes['info']['clubId'], innerRes['info']['clubName'],
                                                      innerRes['applyId']))
                    else:
                        return changeClubState(innerRes['info']['clubId'], 'admit')  # recover the club
                elif infoType == 'joinClub':
                    state = 'joined' if flag else 'refuse'
                    print innerRes['info']
                    isSuccess = changeMemberState(innerRes['info'][u'clubId'], session['studentId'],
                                                  innerRes['applyId'], state)
                    return isSuccess

            res = dealWithPendingInfo(res, res['type'], flag)
            if not res:
                return error('CHECK ERROR')
            res = deletePendingInfo(pendingInfoId, session['studentId'])
            if res is None:
                return error('CHECK ERROR')
            elif res:
                return success()
            else:
                return error('CHECK ERROR')
    else:
        return error('NOT_LOGGED_IN')


@app.route('/api/getPendingInfo', methods=['POST'])
@jsonApi(
)
def getPendingInfo():
    if apiCheckSession():
        res = getPendingInfoByCheckId(session['studentId'])
        return success(info=res)
    else:
        return error('NOT_LOGGED_IN')


# user

@app.route('/api/setPersonalInfo', methods=['POST'])
@jsonApi(
    email=isEmail,
    phone=lenIn(11, 11),
    major=checkMajor,
    sex=checkSex,
    tag=lenIn(0, 12),
    introduction=lenIn(0, 12),
    selfPhoto=isStr
)
def apiSetPersonalInfo(email, phone, major, sex, tag, introduction, selfPhoto):
    if 'studentId' in session:
        nowState = session.get('state', 1)
        res = updatePersonalInfoService(session['studentId'], session['studentName'],
                                        email, phone, major, sex, tag, introduction, selfPhoto, nowState)
        if isStr(res):
            return error(res)
        else:
            session['state'] = res['state']
            return success()
    else:
        return error('NOT_LOGGED_IN')


# @app.route('/api/getPersonalInfo', methods=['POST'])
# @jsonApi(
# )
# def apiGetPersonalInfo():
#     if apiCheckSession():
#         return apiGetSomeoneInfo(session['studentId'])
#     else:
#         return error('NOT_LOGGED_IN')

@app.route('/api/getPersonalInfo', methods=['POST'])
@jsonApi(
    studentId=optional(allChecked(lenIn(10, 10), isAllDigits)),
    full=optional(isBool),
)
def apiGetPersonalInfo(studentId=None, full=False):
    if apiCheckSession(1):
        if studentId is None:
            studentId = session['studentId']
        isThisPerson = (session['studentId'] == studentId)
        if isThisPerson:
            res = getPersonalInfoService(studentId)
        else:
            if not apiCheckSession(2):
                return error('NOT_LOGGED_IN')
            res = getPersonalInfoService(studentId, full)
        res.update({'is_this_person': isThisPerson})
        if isStr(res):
            return error(res)
        return success(info=res)
    else:
        return error('NOT_LOGGED_IN')

@app.route('/api/searchUser', methods=['GET'])
@jsonApi(
    studentId=optional(allChecked(lenIn(10, 10), isAllDigits)),
    studentName=isStr,
)
def apiSearchUser(studentId=None, studentName=None):
    if apiCheckSession(3):
        para = {}
        if studentId:
            para['id'] = studentId
        if studentName:
            para['name'] = studentName
        if not para:
            return  error('ARGUMENTS')
        userInfo = searchUser(para)
        return success(info=userInfo)
    else:
        return error('PERMISSION_DENIED')


@app.route('/api/changeUserLevel', methods=['POST'])
@jsonApi(
    studentId=allChecked(lenIn(10, 10), isAllDigits),
    level=checkLevel,
)
def apiChangeUserLevel(studentId, level):
    if apiCheckSession(3):
        if level == 'common':
            if studentId == session['studentId']:
                return error('USER_LEVEL_CHANGE_FAILED')
            res = changeUserLevelService(studentId, 0)
            addRefreshStateList(studentId) # set new state
        elif level == 'president':
            res = changeUserLevelService(studentId, 1)
        elif level == 'superuser':
            if studentId == session['studentId']:
                res = True
            else:
                res = changeUserLevelService(studentId, 3)
        else:
            res = False
        if not res:
            return error('USER_LEVEL_CHANGE_FAILED')
        else:
            return success()
    else:
        return error('PERMISSION_DENIED')


# miscellaneous
@app.route('/api/getBannedWords', methods=['GET'])
@jsonApi()
def apiGetBannedWords():
    if apiCheckSession(3):
        return success(info=getBannedWords())
    else:
        return error('PERMISSION_DENIED')


@app.route('/api/setBannedWords', methods=['POST'])
@jsonApi(
    bannedWords=isStrList
)
def apiSetBannedWords(bannedWords):
    if apiCheckSession(3):
        res = setBannedWords(banned_words)
        if not res:
            return error('SET_BANNED_WORDS_FAILED')
        else:
            return success()
    else:
        return error('PERMISSION_DENIED')


# @app.route('/api/getAnotherInfo', methods=['POST'])
# @jsonApi(
#     studentId=allChecked(lenIn(10, 10), isAllDigits)
# )
# def apiGetAnotherInfo(studentId):
#     return apiGetSomeoneInfo(studentId)


# def apiGetSomeoneInfo(studentId):
#     res = getPersonalInfoService(studentId)
#     if isStr(res):
#         return error(res)
#     else:
#         return success(info=res)

# this is not POST API, do not need add jsonApi prefix
@app.route('/<staticResource>')
def returnStaticResource(staticResource):
    return app.send_static_file(staticResource)


if __name__ == '__main__':
    initialize()
    app.run(host='127.0.0.1', port=8000, debug=True)
