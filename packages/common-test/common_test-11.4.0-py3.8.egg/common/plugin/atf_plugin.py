from common.plugin.data_plugin import DataPlugin

from common.plugin.file_plugin import FilePlugin

from common.plugin.data_bus import DataBus
from loguru import logger

from common.common.api_driver import APIDriver

from common.common.constant import Constant

from common.data.handle_common import get_system_key


class ATFPlugin(object):

    @classmethod
    def db_ops(self,_key, _sql, env: str=Constant.ENV):
        DataBus.save_init_data()
        if get_system_key(Constant.ENV) is not None:
            env = get_system_key(Constant.ENV)
        sql_type = _sql.strip().split(" ")[0].lower()
        if "select" == sql_type:
            _tempdata = APIDriver.http_request(url=f"{Constant.ATF_URL_API}/querySetResult/{_key}/{env}",
                                               method='post', parametric_key='data', data=_sql,
                                               _log=False)
            logger.error(f"执行sql成功:{_sql}")
            return list(_tempdata.json())
        if "insert" == sql_type or "delete":
            _tempdata = APIDriver.http_request(url=f"{Constant.ATF_URL_API}/doExecute/{_key}/{env}",
                                               method='post', parametric_key='data', data=_sql,
                                               _log=False)
            logger.error(f"执行sql成功:{_sql}")
            return _tempdata
        else:
            logger.error("不支持其他语句类型执行，请检查sql")


if __name__ == '__main__':
    str1 = '{"sql": "select * from tb_major_customer_booking "}'
    DataBus.set_key("env","test")
    print(ATFPlugin.db_ops('CESNDS','select * from tb_major_customer_booking')[0]['BOOKING_ID'])