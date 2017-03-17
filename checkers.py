# -*- coding:utf-8 -*-

from information import *
import validators
import datetime
import pytz


def optional(func):
    def optionalFunc(s):
        if s is None:
            return True
        return func(s)
    return optionalFunc


def isTimestamp(s):
    return isIntIn(0, 10000000000)


def isTimezone(s):
    return s in pytz.all_timezones


def allRight(s):
    return True


def allChecked(*checkers):
    def allCheckedFunc(s):
        for checker in checkers:
            if not checker(s):
                return False
        return True
    return allCheckedFunc


def anyChecked(*checkers):
    def anyCheckedFunc(s):
        for checker in checkers:
            if checker(s):
                return True
        return False
    return anyCheckedFunc


def equals(x):
    def equalsFunc(s):
        return x == s
    return equalsFunc


def isEmail(s):
    return lenIn(5, 128)(s) and validators.email(s) 


def isUrl(s):
    return lenIn(5, 256)(s)


def isPrice(s):
    return isinstance(s, int) or isinstance(s, float)


def isIntIn(minInt, maxInt):
    def intInFunc(s):
        if not isInt(s):
            return False
        return minInt <= s <= maxInt
    return intInFunc


def lenIn(minLen, maxLen):
    def lenInFunc(s):
        if not isStr(s):
            return False
        s = s.strip()
        return minLen <= len(s) <= maxLen
    return lenInFunc


def notEmpty(s):
    return isStr(s) and s.strip()


def isStr(s):
    return isinstance(s, basestring)


def isInt(s):
    return isinstance(s, int) or isinstance(s, long)


def isPositive(s):
    return isinstance(s, int) and s > 0


def isBool(x):
    return x in [True, False]


def isAllDigits(s):
    for i in s:
        if i not in '1234567890':
            return False
    return True


def checkDuringTime(s):
    keys = s.keys()
    time_keys = ['year', 'month', 'day', 'shour', 'sminute', 'hour', 'minute']
    for key in time_keys:
        if key not in keys:
            return False
        else:
            if isInt(s[key]) is not True:
                return False
    now_time = datetime.datetime.now()
    # print now_time
    date = str(s['year']) + '-' + str(s['month']) + '-' + str(s['day'])
    start_t = str(s['shour']) + ':' + str(s['sminute']) + ':0'
    start_time = datetime.datetime.strptime(' '.join([date, start_t]), "%Y-%m-%d %H:%M:%S")
    # print start_time
    # end_t = str(s['hour']) + ':' + str(s['minute']) + ':0'
    # end_time = datetime.datetime.strptime(' '.join([date, end_t]), "%Y-%m-%d %H:%M:%S")
    # print end_time
    interval_n_s = (start_time - now_time).total_seconds() / 60
    # interval_s_e = (end_time - start_time).total_seconds()
    # if interval_n_s < 30 and interval_s_e > 0:
    if interval_n_s < 30 or s['minute'] >= 60:
        return False
    return True


def checkType(s):
    if all([i in sports_type for i in s]):
        return True
    else:
        return False


def checkLeader(s):
    keys = s.keys()
    leader_keys = ['id', 'name']
    for key in leader_keys:
        if key not in keys:
            return False
        else:
            if isStr(s[key]) is not True:
                return False
    return True


def checkCreateTime(s):
    keys = s.keys()
    time_keys = ['year', 'month', 'day']
    for key in time_keys:
        if key not in keys:
            return False
        else:
            if isInt(s[key]) is not True:
                return False
    return True


def checkMajor(s):
    print s
    if s in major_type.keys():
        return True
    else:
        return False


def checkSex(s):
    print s
    if s in sex:
        return True
    else:
        return False


def checkFlag(s):
    if s in flag:
        return True
    else:
        return False


def checkCapacity(s):
    if isPositive(s):
        if s <= 100:
            return True
    return False


if __name__ == '__main__':
    # try:
    #     datetime.date(2011, 2, 29)
    #     print 1
    # except Exception, e:
    #     print 2
    checkDuringTime({
        'year': 2016,
        'month': 12,
        'day': 12,
        'shour': 12,
        'sminute': 30,
        'ehour': 13,
        'eminute': 30
    })
