# -*- coding:utf-8 -*-

from connector import Mongo
from utils import traitAttr
import parameter
import datetime

'''
    collection: club
    porpuse: store the information of club
    data type: json
    example of data structure:
    {
        "id": <digits string(5)>,
        "name": <string>,
        "createTime": {"year":<int>, "month":<int>, "day":<int>},
        "type": <string>,
        "introduction": <string>,
        "leader":{
            "id": <string>,
            "name": <string>
        }
        "managers": [{
            "id":<string>,
            "name":<string>,
        },...],
        "members": [{
            "id":<string>,
            "name":<string>,
            "phone": <digits string(11)>,
            "major": <enum string>,
            'introduction': <string>,
            'selfPhoto': <string>
            "state":<enum string> ['not_join', 'apply', 'joined', 'refuse', 'quit']
        },...],
        "major": <enum string> ['计算机系', '电子系', '社科学院', '土木系']
        "state": <enum string> ['pending', 'admit', 'delete', 'refuse']
        "reason": <string>
    }
'''

def addManagerService(clubId, clubName, applyId, state):
    if state == 'refuse':
        return True
    manageList = {
        'clubId': clubId,
        'clubName':clubName
    }
    res = Mongo.user.find_and_modify(
        query={
            'id': applyId
        },
        update={
            '$addToSet': {'manager': manageList}
        },
        upsert=False,
        full_response=True,
        new=True
    )
    print 'addManagerService res: ', res
    if res['ok']:
        if res['value'] is None:
            return None
        else:
            return res['value']
    else:
        return False

def delManagerService(clubId, clubName, applyId):
    manageList = {
        'clubId': clubId,
        'clubName':clubName
    }
    res = Mongo.user.find_and_modify(
        query={
            'id': applyId
        },
        update={
            '$pull': {'manager': {"clubId": clubId}}
        },
        upsert=False,
        full_response=True,
    )
    print 'delManagerService res: ', res
    if res['ok']:
        if res['value'] is None:
            return None
        else:
            return res['value']
    else:
        return False




def listClubsService(skip, limit, para={}):
    return [traitAttr(i, {
        'id': '', 'name': '', 'type': '', 'motto': '', 'major': '', 'leader': '',
        'scale': len(filterMember(i['members'], ['joined'])), 'state': '',
    }) for i in Mongo.club.find(para).skip(skip).limit(limit).sort('members', {'$size': 1})]


def getClubService(id, stateList):
    res = Mongo.club.find_one({'id': id})
    if res is None:
        return 'CLUB_NOT_EXIST'
    res = separateMember(res, stateList)
    # res['members'] = [i.update({'motto': ''}) for i in res['members']]
    # res['managers'] = [i.update({'motto': ''}) for i in res['managers']]
    return traitAttr(res, {
        'id': '', 'name': '', 'type': '', 'motto':'', 'remark': '', 'introduction': '', 'state': 'pending',
        'poster': '', 'leader': {'id': '', 'name': '', 'phone': '', 'major': ''}, 'managers': [], 'members': [],
        'major': '', 'scale': len(res['members']) + len(res['managers']) + 1
    })


def filterMember(members, stateList):
    # print members, stateList
    return filter(lambda x: x['state'] in stateList, members)



def separateMember(info, stateList):
    info['members'] = filterMember(info['members'], stateList)
    # print info['members']
    [info['managers'], info['members']] = separate(info['managers'], info['members'])
    [leader, info['managers']] = separate([info['leader']], info['managers'])
    # print leader
    info['leader'] = leader[0]
    return info


def separate(sub, total):
    subId = [i['id'] for i in sub]
    # print sub, total
    # print subId
    sub = filter(lambda x: x['id'] in subId, total)
    notSub = filter(lambda x: x['id'] not in subId, total)
    # print sub, notSub
    return [sub, notSub]


# return: 0: create failed; 1:create succeeded; 2: club name existed
def createClubService(clubId, name, type, major, motto, remark, introduction, poster, leader, manager, member):
    nameExist = Mongo.club.find_one({"name": name, "major": major})
    if nameExist is not None:
        return 2
    # clubId = str(int(parameter.getAndUpdateClubId())).zfill(5)
    clubIdExist = Mongo.club.find_one({'id': clubId})
    if clubIdExist is not None:
        return 3
    now_time = datetime.datetime.now()
    createTime = {
        'year': int(now_time.year),
        'month': int(now_time.month),
        'day': int(now_time.day)
    }
    info = {
        'id': clubId,
        'name': name,
        'createTime': createTime,
        'type': type,
        'major': major,
        'motto': motto,
        'remark': remark,
        'introduction': introduction,
        'poster': poster,
        'leader': leader,
        'managers': [manager],
        'members': [member],
        'state': 'pending'
    }
    res = Mongo.club.insert_one(info)
    if res is None:
        return 0
    return 1


def deleteClubService(clubId):
    res = Mongo.club.remove({'id': clubId})
    if res['n'] == 1:
        return True
    else:
        return False


def joinClubService(cludId, member):
    res = Mongo.club.find_and_modify(
        query={
            'id': cludId
        },
        update={
            '$addToSet': {'members': member}
        },
        upsert=False,
        full_response=True,
        new=True
    )
    if res['ok']:
        if res['value'] is None:
            return None
        else:
            return res['value']
    else:
        return False


def quitClubService(cludId, memberId):
    res1 = Mongo.club.find_and_modify(
        query={
            'id': cludId
        },
        update={
            '$pull': {'manager': {'id': memberId}}
        },
        upsert=False,
        full_response=True,
        new=True
    )
    res2 = Mongo.club.find_and_modify(
        query={
            'id': cludId,
            'members.id': memberId
        },
        update={
            '$set': {
                'members.$.state': 'quit'
            }
        },
        upsert=False,
        full_response=True,
        new=True
    )
    if res1['ok'] and res2['ok']:
        if res1['value'] is None or res2['value'] is None:
            return False
        else:
            return True
    else:
        return False



def changeMemberState(clubId, managerId, memberId, state):
    res = Mongo.club.find_one({'id': clubId, 'managers.id': managerId})
    if res is None:
        return False
    res = Mongo.club.find_and_modify(
        query={
            'id': clubId,
            'members.id': memberId
        },
        update={
            '$set': {
                'members.$.state': state
            }
        },
        upsert=False,
        full_response=True,
        new=True
    )
    if res['ok']:
        if res['value'] is None:
            return None
        else:
            return True
    else:
        return False


def changeClubState(clubId, state, reason=""):
    res = Mongo.club.find_and_modify(
        query={
            'id': clubId
        },
        update={
            "$set": {
                'state': state,
                'reason': reason,
            }
        },
        upsert=False,
        full_response=True,
        new=True
    )
    if res['ok']:
        if res['value'] is None:
            return None
        else:
            return True
    else:
        return False


def updateClubInfoService(studentId, studentName, clubId, clubName, type, introduction, major):
    if not searchManager(clubId, studentId):
        return 'PERMISSION_DENIED'
    res = Mongo.club.find_and_modify(
        query={
            'id': clubId,
            'managers.id': studentId,
            'managers.name': studentName
        },
        update={
            "$set": {
                'name': clubName,
                'type': type,
                'introduction': introduction,
                'major': major
            }
        },
        upsert=False,
        full_response=True,
        new=True
    )
    if res['ok']:
        if res['value'] is None:
            return 'CLUB_INFORMATION_MODIFY_FAILED'
        else:
            return True
    else:
        return 'CLUB_INFORMATION_MODIFY_FAILED'


def searchMember(clubId, memberId):
    res = Mongo.club.find_one({'id':clubId}, {'members': 1})
    if res is None:
        return False
    for member in res['members']:
        if member['id'] == memberId and member['state'] == 'joined':
            return True
    return False


def searchManager(clubId, managerId):
    res = Mongo.club.find_one({'id':clubId}, {'managers': 1})
    if res is None:
        return False
    for manager in res['managers']:
        if manager['id'] == managerId:
            return True
    return False


def searchLeader(clubId, leaderId):
    res = Mongo.club.find_one({'id':clubId}, {'leader': 1})
    print res
    if res is None:
        return False
    if res['leader']['id'] == leaderId:
        return True
    return False

def getLeader(clubId):
    res = Mongo.club.find_one({'id': clubId}, {'leader': 1})
    if res is None:
        return None
    else:
        return res['leader']


def getMajor(clubId):
    res = Mongo.club.find_one({'id': clubId}, {'major': 1})
    if res is None:
        return None
    else:
        return res['major']


def changeClubLeaderService(clubId, leaderId, leaderName):
    clubInfo = getClubService(clubId, [])
    if not clubInfo:
        return None
    else:
        newLeader = {'id': leaderId, 'name': leaderName}
        updateRes = Mongo.club.update_one(
            {'id': clubId},
            {'$set': {
                'leader': newLeader,
                'manager': newLeader,
            }}
        )
        res = delManagerService(clubId, '', clubInfo['leader']['id']) and \
              addManagerService(clubId, clubInfo['name'], leaderId, 'admit') and \
              updateRes and updateRes['modified_count']
        if not res:
            return False
        else:
            return True



if __name__ == '__main__':
    t_name = '小白粉丝群'
    t_createTime = {'year': 2016, 'month': 12, 'day': 12}
    t_type = ['运动']
    t_introduction = '小白的粉丝聚集地'
    t_major = ''
    manager = {'id': '2013012345', 'name': '大白'}
    # now_time = datetime.datetime.now()
    # print now_time.year, now_time.month, now_time.day, now_time.hour, now_time.minute, now_time.second
    # print createClubService(t_name, t_createTime, t_type, t_introduction, t_major, manager)
    # print getClubService("00004")
    # print joinClubService('00004', '2013012349', '徐涵')
    # print changeMemberState('00004', '2013012345', '2013012001', 'joined')
    print deleteClubSerive('201632004')
