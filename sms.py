# coding=utf-8

__author__ = 'JasonLee'


# 如有问题 联系 张叔阳 zhangshuyang@outlook.com 18810456305
import requests
import json
import datetime
from appConfig import celery


AUTH_KEY = "key-56cf73ec3cd1df1f2716b3f901e6c14c"   ### 这只是一个示例，并不是真实的，如果你注册了螺丝帽的账号就会生成一个authkey
MOBILE = "18810967211"   ## 接收人的手机号
TEXT = str(datetime.datetime.now()) + "现在又来一次!【咚咚体育】"  ###要发送的内容，注意尾部一定要加上 中文（全角）的方括号，里面写账户信息， api就是通过这个和authkey来确认身份的

def send_messag_example():
    resp = requests.post("http://sms-api.luosimao.com/v1/send.json",
                         auth=("api", AUTH_KEY),
                         data={
                             "mobile": MOBILE,
                             "message": TEXT
                         },timeout=3 , verify=False)
    result =  json.loads( resp.content )
    return result

def send_batch(phones, content):
    resp = requests.post("http://sms-api.luosimao.com/v1/send_batch.json",
                        auth=("api", AUTH_KEY),
                        data={
                            "mobile_list": phones,
                            "message": content
                        },timeout=3 , verify=False)
    result =  json.loads( resp.content )
    return result['error'], result['msg']


@celery.task(name='delete_notify')
def notify_delete_activity(activity, by_superuser, reason):
    name = activity['name']
    event = u"管理员删除" if by_superuser else u"发起者取消"
    content = u"您参加的活动：%s已被%s。" % (name, event)
    if by_superuser and reason:
        if isinstance(reason, str):
            reason = reason.decode('utf8')
        content += u"删除原因：%s" % reason
    phone_list = [one['phone'] for one in activity['participants']]
    if by_superuser:
        phone_list.append(activity['leader']['phone'])
    if not phone_list:
        return True
    code, msg = send_batch(phone_list, content)
    if code == 0:
        return True
    else:
        print activity['id'], activity['name'], 'send fail', msg
        return False


# def send_batch(phones, content):
#     print "success___",
#     return 0, 'lala'

# CONTROL = False   #####  这里写你要写的后台的业务逻辑
#
# if CONTROL:
#     print send_messag_example()   ## 也可以不print，这个函数返回值是 api的response，里面有状态码，失败信息什么的