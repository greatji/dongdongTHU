from flask import jsonify, request
from functools import wraps
from errors import *
import json
import datetime


def traitAttr(dictObj, selector):
    if dictObj is None:
        return dictObj
    res = {}
    for k in selector:
        res[k] = dictObj.get(k, selector[k])
    return res


def checkOneField(jsonObj, key, checker, errs=None):
    if key in jsonObj:
        res = checker(jsonObj[key])
        if not res:
            print key, res
            if errs is not None:
                errs.append(key)
        return res
    print key, "not found"
    res = checker(None)
    if (not res) and (errs is not None):
        errs.append(key)
    return res

def get_datetime(s):
    date = str(s['year']) + '-' + str(s['month']) + '-' + str(s['day'])
    start_t = str(s['shour']) + ':' + str(s['sminute']) + ':0'
    start_time = datetime.datetime.strptime(' '.join([date, start_t]), "%Y-%m-%d %H:%M:%S")
    return start_time


class jsonApi(object):

    checkers = None

    def __init__(self, **checkers):
        self.checkers = checkers

    def __call__(self, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if request.method != 'GET':
                j = None
                try:
                    j = json.loads(request.data)
                except ValueError, e:
                    print e
                    return jsonify(error('JSON_PARSE'))
                errs = []
                if not all([checkOneField(
                        j, k, v, errs) for k, v in self.checkers.iteritems()]):
                    return jsonify(error('ARGUMENTS', remark=errs))
                kwargs.update(
                    {k: j[k] for k in self.checkers if k in j})
            return jsonify(func(*args, **kwargs))
        return wrapped

# test

if __name__ == '__main__':
    assert traitAttr({'a':1, 'b':2, 'c':3}, {'a':3, 'd':3}) == {'a':1, 'd':3}
    assert traitAttr(None, {}) == None
    assert traitAttr([1,2,3,4], {}) == [1,2,3,4]
    assert traitAttr({'a':1, 'b':2}, {}) == {}