# -*- coding:utf-8 -*-

from connector import Mongo
import parameter

'''
    collection: pendInfo
    purpose: store the information of user
    data type: json
    example of data structure:
    {
        "id": <digits string(20)>, // 审核号长度
        "applyId": <digits string(10)>, // 申请者学号
        "applyName": <string>, //申请者姓名
        "checkId": [<digits string(10)>], // 审核者学号列表
        "type": <enum string> ['joinClub', 'deleteClub', 'createClub'], // 审核信息类型
        "info":{    // 附加信息
            case 'joinClub', deleteClub, createClub: {
                clubId: <digits string(5)>,
                clubName: <string>
            }
        }
    }
'''


def createPendingInfo(applyId, applyName, checkId, type, info):
    res = Mongo.pendInfo.find_one({
        'applyId': applyId,
        'applyName': applyName,
        'checkId': checkId,
        'type': type,
        'info': info
    })
    print res
    if res is not None:
        return True
    pendingInfoId = str(int(parameter.getAndUpdatePendingInfoId())).zfill(15)
    pendingInfo = {
        'id': pendingInfoId,
        'applyId': applyId,
        'applyName': applyName,
        'checkId': checkId,
        'type': type,
        'info': info
    }
    res = Mongo.pendInfo.insert_one(pendingInfo)
    if res is None:
        return False
    return True


def getPendingInfoByCheckId(checkId):
    res = Mongo.pendInfo.find({
        'checkId': checkId
    })
    all_res = []
    for i in res:
        temp = {
            'id': i['id'],
            'applyId': i['applyId'],
            'applyName': i['applyName'],
            'info': i['info'],
            'type': i['type']
        }
        all_res.append(temp)
    return all_res


def getPendingInfoByPendingInfoId(pendingInfoId, checkId):
    res = Mongo.pendInfo.find_one({
        'id': pendingInfoId,
        'checkId': checkId
    })
    return res


def deletePendingInfo(pendingInfoId, checkId):
    res = Mongo.pendInfo.remove({
        'id': pendingInfoId,
        'checkId': checkId
    })
    if res is None:
        return None
    elif res['ok'] == 1:
        return True
    else:
        return False


def deletePendingInfoByClubId(clubId):
    res = Mongo.pendInfo.remove({
        'info.clubId': clubId
    })
    if res['n'] == 1:
        return True
    else:
        return False


if __name__ == '__main__':
    applyId = '2013002001'
    applyName = 'donghy'
    checkId = ['2013000001', '2013001011']
    m_type = 'joinClub'
    info = {'clubId': '00002', 'clubName': '篮球俱乐部'}
    # createPendingInfo(applyId, applyName, checkId, m_type, info)
    # deletePendingInfo('000000000000005', '2013001011')
    # getPendingInfoByCheckId('2013001011')
    # print getPendingInfoByPendingInfoId('000000000000009', '2013001011')
    deletePendingInfoByClubId('201632004')
