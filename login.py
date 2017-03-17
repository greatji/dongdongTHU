# -*- coding:utf-8 -*-

from connector import Mongo


def login(studentId, password):
    res = Mongo.login.find_one({'id': studentId, 'password': password})
    return res


if __name__ == '__main__':
    # print login('2013012345', '2013012345')
    # print login('20130110010', '2013011001')
    # info = {
    #     'id': '2013011000',
    #     'password': '2013011000',
    #     'name': '张三'
    # }
    info = {
        'id': '2013011007',
        'password': '2013011007',
        'name': '郑十'
    }
    Mongo.login.insert(info)
