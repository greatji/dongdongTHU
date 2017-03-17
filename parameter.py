# -*- coding:utf-8 -*-

from connector import Mongo
from information import major_type

'''
    collection: parameter
    purpose: storage the information of some global parameter
    data type: json
    example of data structure:
    {
        "id": <int>
    }
'''


def getAndUpdateActivityId():
    res = Mongo.parameter.find_and_modify(
        query={'type': 'global'},
        update={"$inc": {"activityId": 1}},
        upsert=False,
        full_response=True
    )
    return res[u'value'][u'activityId']


def getAndUpdateClubId(major):

    res = Mongo.parameter.find_and_modify(
        query={'type': 'global'},
        update={"$inc": {"clubId." + major_type[major]: 1}},
        upsert=False,
        full_response=True
    )
    return res[u'value'][u'clubId'][major_type[major]]


def getAndUpdatePendingInfoId():
    res = Mongo.parameter.find_and_modify(
        query={'type': 'global'},
        update={"$inc": {"pendingInfoId": 1}},
        upsert=False,
        full_response=True
    )
    return res[u'value'][u'pendingInfoId']


def createParameter():
    major_id = {major_type[major]: 1 for major in major_type.keys()}
    res = Mongo.parameter.find_and_modify(
        query={'type': 'global'},
        update={"$set": {"clubId": major_id, "activityId": 1, "pendingInfoId": 1}},
        upsert=False,
        full_response=True
    )
    return res


if __name__ == '__main__':
    # getAndUpdateActivityId()
    # print getAndUpdateClubId(u'计算机系')
    print createParameter()
