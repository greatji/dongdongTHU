# coding=utf-8
from connector import Mongo
from sms import send_batch
import datetime

__author__ = 'JasonLee'


def sms_content(one):
    name = one['name']
    place = one['address']
    time = one['startTimestamp']
    return u"您参加的活动：%s（%s，%s点%s分），就要开始咯！【咚咚体育】" % (name, place, time.hour, time.minute)


def batch_notify(activity_id, phone_list, content):
    phones = ",".join(phone_list)
    code, msg = send_batch(phones, content)
    if code == 0:
        return True
    else:
        print datetime.datetime.now(), activity_id, msg
        return False


def sms_task():
    now = datetime.datetime.now()
    half_hour = datetime.timedelta(minutes=30)
    future_limit = now + half_hour
    activities = Mongo.activity.find({
        'startTimestamp':
            {"$gte": now, "$lte": future_limit},
        "sms_send":
            {"$ne": 1},
        "state": "open",
    }).sort("startTimestamp", -1)

    if activities is None or activities.count() == 0:
        return

    else:
        success_ids = []
        for one in activities:
            phones = []
            phones.append(one['leader']['phone'])
            for p in one['participants']:
                phones.append(p['phone'])

            content = sms_content(one)
            if batch_notify(one['id'], phones, content):
                success_ids.append(one['id'])

        Mongo.activity.update_many(
            {
                "id": {"$in": success_ids}
            },
            {
                "$set": { "sms_send": 1}
            },
        )



def print_lala():
    print 'lala'