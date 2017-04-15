# -*- coding:utf-8 -*-

from connector import Mongo
from utils import traitAttr, get_datetime
import parameter
import datetime
from errors import error_num

'''
    collection: activity
    purpose: storage the information of activity
    data type: json
    example of data structure:
    {
        "id": <digits string(7)>,
        "name": <string>,
        "duringTime": {"year":<int>, "month":<int>, "day":<int>, "shour":<int>, "sminute":<int>, "hour":<int>, "minute":<int>},
        "startTimestamp": <Date(UTC datetime)> // save local time representation, not utc
        "address": <string>,
        "capacity": <int>,
        "type": [<enum string>],
        "introduction": <string>,
        'poster': <string>,
        'state':<enum string>, ['open', 'close']
        "leader": {
            'id':<string>,
            'name':<string>,
            'phone':<digits string<11>>,
            'major':<enum string>,
            'introduction':<string>,
            'selfPhoto':<string>
        }
        "participantsSum": <int>,
        "participants": [{
            'id':<string>,
            'name':<string>,
            'phone':<digits string<11>>,
            'major':<enum string>,
            'introduction':<string>,
            'selfPhoto':<string>
        },...]
        comments: {
            'studentName': <string>,
            'content': <string>
        }
        'filterMajors': [<enum string: major>] // 允许加入的院系
    }
'''


def listActivitiesService(skip, limit, para={}):
    res = [traitAttr(i, {
        'id':'', 'name':'', 
        'duringTime':{'year':0, 'month':0, 'day':0, 'shour':0, 'sminute':0, 'hour':0, 'minute':0},
        'address':'', 'capacity':0, 'leader':{'name':'', 'id':''}, 'introduction':'', 'type':[],
        'participantsSum': len(i['participants']) + 1, 'state': 'close'
    }) for i in Mongo.activity.find(para).skip(skip).limit(limit).sort(
        [('duringTime.year', -1), ('duringTime.month', -1), ('duringTime.day', -1), ('duringTime.shour', -1),
         ('duringTime.sminute', -1), ('duringTime.hour', -1), ('duringTime.minute', -1)])]
    print res
    return res


def getActivityService(activityId):
    checkActivityState(activityId)
    res = Mongo.activity.find_one({'id': activityId})
    if res is None:
        return None
    new_res = traitAttr(res, {
        'id': '', 'name': '',
        'duringTime': {'year': 0, 'month': 0, 'day': 0, 'shour': 0, 'sminute': 0, 'hour': 0, 'minute': 0},
        'address': '', 'capacity': 0, 'type': [], 'introduction': '', 'state': 'close',
        'leader': {'name': '', 'id': '', 'phone': '', 'major': '', 'selfPhone': ''},
        'participants': [], 'participantsSum': len(res['participants']) + 1, 'filterMajors':[],
    })
    if len(res['comments']) != 0:
        new_res['comments'] = res['comments']
    return new_res


def createActivityService(name, duringTime, address, capacity, type, introduction, leader, poster, filterMajors=None):
    activityId = str(int(parameter.getAndUpdateActivityId())).zfill(5)
    info = {
        'id': activityId,
        'name': name,
        'duringTime': duringTime,
        'startTimestamp': get_datetime(duringTime),
        'address': address,
        'capacity': capacity,
        'type': type,
        'introduction': introduction,
        'leader': leader,
        'poster': poster,
        'state': 'open',
        'participants': [],
        # 'participantsSum': 1,
        'comments': []
    }
    if filterMajors:
        info['filterMajors'] = filterMajors
    res = Mongo.activity.insert_one(info)
    if res is None:
        return False
    return True


def deleteActivityService(activityId):
    res = Mongo.activity.remove({'id': activityId})
    if res['n'] == 1:
        return True
    else:
        return False


def addParticipant(activityId, participant):
    wheatherOpen = checkActivityState(activityId)
    print wheatherOpen
    if not wheatherOpen:
        return False
    res = Mongo.activity.find_one({'id': activityId, 'participants.id': participant['id']})
    print res
    if res is not None:
        return True
    capacity = Mongo.activity.find_one({'id': activityId}, {"capacity": 1, 'filterMajors': 1})
    # print '--------------------'
    # print capacity
    if capacity['capacity'] == 1:
        return error_num('ACTIVITY_FULL')
    if 'filterMajors' in capacity and participant['major'] not in capacity['filterMajors']:
        print capacity['filterMajors'],"==================="
        return error_num('ACTIVITY_MAJOR_NOT_MATCH')
    res = Mongo.activity.find_and_modify(
        query={
            'id': activityId,
            'participants.' + str(capacity['capacity'] - 2): {"$exists": 0}
        },
        update={
            '$addToSet': {'participants': participant}
        },
        upsert=False,
        full_response=True,
        new=True
    )
    print res
    if res['ok']:
        if res['value'] is not None:
            return traitAttr(res['value'], {
                'participants': [], 'participantsSum': 0
            })
        else:
            return error_num('ACTIVITY_FULL')
    else:
        return False


def quitActivityService(activityId, studentId):
    if not checkActivityState(activityId):
        return False
    res = Mongo.activity.find_and_modify(
        query={
            'id': activityId
        },
        update={
            '$pull': {'participants': {'id': studentId}}
        },
        upsert=False,
        full_response=True,
        new=True
    )
    if res['ok']:
        if res['value'] is None:
            return False
        else:
            return True
    else:
        return False


def updateActivityInfoService(activityId, studentId, studentName, name, duringTime, address, capacity, type, introduction):
    if not searchOrganizer(activityId, studentId):
        return 'PERMISSION_DENIED'
    res = Mongo.activity.find_and_modify(
        query={
            'id': activityId,
            'leader.id': studentId,
            'leader.name': studentName
        },
        update={
            "$set": {
                'name': name,
                'duringTime': duringTime,
                'startTimestamp': get_datetime(duringTime),
                'address': address,
                'capacity': capacity,
                'type': type,
                'introduction': introduction
            }
        },
        upsert=False,
        full_response=True,
        new=True
    )
    print res
    if res['ok']:
        if res['value'] is None:
            return 'ACTIVITY_INFORMATION_MODIFY_FAILED'
        else:
            return True
    else:
        return 'ACTIVITY_INFORMATION_MODIFY_FAILED'


def searchParticipant(activityId, participantId):
    res = Mongo.activity.find_one({'id': activityId}, {'participants': 1})
    if res is None:
        return False
    for participant in res['participants']:
        if participant['id'] == participantId:
            return True
    return False


def searchOrganizer(activityId, leaderId):
    res = Mongo.activity.find_one({'id': activityId}, {'leader': 1})
    if res is None:
        return False
    if res['leader']['id'] == leaderId:
        return True
    return False


def addComment(studentName, activityId, commentContent):
    res = Mongo.activity.find_and_modify(
        query={
            'id': activityId
        },
        update={
            '$addToSet': {
                'comments': {
                    'studentName': studentName,
                    'content': commentContent
                }
            }
        },
        upsert=False,
        full_response=True,
        new=True
    )
    if res['ok'] == 1:
        if res['value'] is None:
            return 'COMMENT_FAILED'
        else:
            new_res = traitAttr(res['value'], {
                'id': '', 'name': '',
                'duringTime': {'year': 0, 'month': 0, 'day': 0, 'shour': 0, 'sminute': 0, 'hour': 0, 'minute': 0},
                'address': '', 'capacity': 0, 'type': [], 'introduction': '',
                'leader': {'name': '', 'id': '', 'phone': '', 'major': '', 'selfPhone': ''},
                'participants': [], 'participantsSum': len(res['participants'])
            })
            if len(res['value']['comments']) != 0:
                new_res['comments'] = res['value']['comments']
            else:
                return 'COMMENT_FAILED'
            return new_res
    else:
        return 'COMMENT_FAILED'


def checkActivityState(activityId):
    res = Mongo.activity.find_one({'id': activityId})
    if res is None:
        return False
    else:
        duringTime = res['duringTime']
        if res['state'] == 'open':
            openTime = datetime.datetime.strptime('-'.join([str(duringTime['year']),
                                                            str(duringTime['month']),
                                                            str(duringTime['day'])]) +
                                                  ' ' +
                                                  ':'.join([str(duringTime['shour']),
                                                            str(duringTime['sminute']), '0']),
                                                  '%Y-%m-%d %H:%M:%S')
            if (datetime.datetime.now() - openTime).total_seconds() >= (duringTime['hour'] * 3600 + duringTime['minute'] * 60):
                Mongo.activity.find_and_modify(
                    query={
                        'id': activityId
                    },
                    update={
                        '$set': {
                            'state': 'close'
                        }
                    }
                )
                return False
            else:
                return True
        else:
            return False


if __name__ == '__main__':
    t_name = '游泳嘉年华'
    t_duringTime = {
        'year': 2016, 'month': 12, 'day': 4, 'shour': 10, 'sminute': 10, 'hour': 12, 'minute': 10
    }
    t_address = '清华大学陈明游泳馆'
    t_capacity = 50
    t_type = ['游泳']
    t_introduction = '互动教学'
    t_leader = {'id': '2013011002', 'name': '王五'}
    # createActivityService(t_name, t_duringTime, t_address, t_capacity, t_type, t_introduction, t_leader)

    # print addParticipant('0000003', participantId='2013012001', participantName='张三')
    # print getActivityService('0000003')
    # print searchParticipant('0000003', '2013011125')
    studentName = '张三'
    activityId = '0000004'
    content = 'LBJ 好厉害,下次还想参加'
    addComment(studentName, activityId, content)
