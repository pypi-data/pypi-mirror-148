import os

from common.common.constant import Constant
from common.plugin.data_bus import DataBus
from common.plugin.file_plugin import FilePlugin
from common.common.api_driver import APIDriver


class ServicePlatForm(object):

    @classmethod
    def sendMsg(self,content, _list):
        for _index in range(len(_list)):
            _arr = str(_list[_index]).split('&')
            os.environ['toUserId'] = str(_arr[0]).lower()
            os.environ['toMail'] = str(_arr[1])
            DataBus.set_key('content',content)
            _data=FilePlugin.load_file("muc.xml").encode()
            APIDriver.http_request(url=DataBus.get_key(Constant.MSG_URL),method='post',parametric_key='data',data=_data)

if __name__ == '__main__':
    DataBus.set_key('msgapi','http://msgapi.ceair.com:8080/msgbuss/soap/sendMessage?wsdl')
    DataBus.set_key('msgtoken','2812de40-af1d-40f3-a0c2-1eb21508a262')
    DataBus.set_key('msgid','S00005520')
    DataBus.set_key('fromUserId','oushiqiang')
    buildurl='http://baidu.com'
    build_report='http://baidu.com'
    _desc = f'项目名称：XXX \n  总用例数：100  \n 失败用例数：10  \n ' \
            f'通过用例数：90  \n 构建详情： {buildurl} \n 执行结果：{build_report}'
    _list='oushiqiang&oushiqiang@ceair.com','XUJINGSI&XUJINGSI@ceair.com'
    print(ServicePlatForm.sendMsg(_desc,_list))

