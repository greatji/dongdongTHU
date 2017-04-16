# -*- coding:utf-8 -*-

from connector import Mongo
from utils import traitAttr

'''
    collection: user
    porpuse: store the information of user
    data type: json
    example of data structure:
    {
        "id": <string: ID number>, // 学号
        "email": <email: string>,
        "phone": <digits string>, 
        "name": <string>, // 姓名
        "major": <string>, // 专业
        "class": <string>,
        "address": <string>,
        "introduction": <string>,
        "times": <int>, // 参加活动的次数
        "tag": <string>, // 个人兴趣点
        "sex": <enum string>, // 性别
        "stage": <int>, // 登陆阶段
        "manager": [{
            clubId: <string>,
            clubName: <string>
            }], // 是某俱乐部的负责人，不是则为空
        "president": [<enum string: major>], // 是某院系的负责人，不是则为空
        "club": [{
            clubId: <string>,
            clubName: <string>
            }], // 参加的俱乐部
        "activity": [{
            activityId: <digits string>,
            activityName: <string>
            }] // 参加的活动
    }
'''


def createPersonalInfoService(id, name):
    res = getPersonalInfoService(id)
    if res == 'NO_SUCH_USER':
        res = Mongo.user.insert_one({
            'id': id,
            'name': name,
            'state': 1,
            'selfPhoto': '',
            'times': 0
        })
        if res is None:
            return 0
        return 1
    else:
        return res['state']


def getPersonalInfoService(studentId, full=True):
    res = Mongo.user.find_one({'id': studentId})
    if res is None:
        return 'NO_SUCH_USER'
    else:
        info = traitAttr(res, {
            'id': '', 'name': '', 'sex': '', 'email': '', 'phone': '', 'major': '', 'introduction': '', 'times': 0,
            'tag': '', 'state': 0, 'selfPhoto': '', 'manager': [],
        })
        if full:
            return info
        else:
            info.update(email='', phone='')
            return info



def updatePersonalInfoService(id, name, email, phone, major, sex, tag, introduction, selfPhoto):
    print id, name
    res = Mongo.user.find_and_modify(
        query={
            'id': id,
            'name': name
        },
        update={
            "$set": {
                'email': email,
                'phone': phone,
                'major': major,
                'sex': sex,
                'introduction': introduction,
                'tag': tag,
                'state': 2,
                'selfPhoto': selfPhoto,
                'president': []
            }
        },
        upsert=False,
        full_response=True,
        new=True
    )
    print res
    if res['ok']:
        if res['value'] is None:
            return 'USER_INFORMATION_MODIFY_FAILED'
        else:
            return True
    else:
        return 'USER_INFORMATION_MODIFY_FAILED'


def updateTimes(id, delta):
    res = Mongo.user.update({"id": id}, {"$inc": {"times": delta}})
    if res['n'] == 1:
        return True
    else:
        return False


def getPresidentOfMajor(major):
    res = Mongo.user.find({'president': major})
    return [traitAttr(i, {
        'id': ''
    }) for i in res]


def isManager(studentId):
    res = Mongo.user.find_one({'id': studentId, 'manager': {'$exists': True}})
    if res is None:
        return False
    else:
        return True


if __name__ == '__main__':
    id = u"2013012444"
    phone = "18812345010"
    email = phone + "@126.com"
    name = u"易坤"
    major = u"计算机系"
    manager = []
    president = [u"计算机系"]
    club = []
    activity = []
    introduction = u"好好学习,天天向上"
    interests = ['游泳']
    address = '紫荆公寓8号楼'
    sex = u'女'
    tag = u'balabala'
    selfPhoto = ''
    # setPersonalInfoService(id=id, email=email, phone=phone, name=name, major=major, manager=manager, president=president, club=club, activity=activity)
    # print getPersonalInfoService('2013011001')
    # updatePersonalInfoService(id, name, email, phone, major, sex, tag, introduction, selfPhoto)
    # print createPersonalInfoService(id, name)
    # updateTimes("2013011356", 1)
    Mongo.user.update({"id": '2013011356'}, {"$set": {"president": [u'计算机系']}})
