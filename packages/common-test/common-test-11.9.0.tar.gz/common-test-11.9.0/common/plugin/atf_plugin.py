from loguru import logger

from common.data.handle_common import get_system_key, set_system_key

from common.plat.jira_platform import JiraPlatForm

from common.plugin.data_bus import DataBus
from common.common.constant import Constant
from common.plat.ATF_platform import ATFPlatForm


class ATFPlugin(object):

    @classmethod
    def db_ops(self,_key, _sql, env: str=Constant.ENV):
        DataBus.save_init_data()
        return ATFPlatForm.db_ops(_key, _sql, env)

    @classmethod
    def sendResult(self):
        if get_system_key('runtype') is not None:
            jirakey=get_system_key('issueKey')
            prjectname=get_system_key('name')
            joburl=get_system_key('JOB_URL')
            buildurl=get_system_key('BUILD_URL')
            jobName_url=joburl+"/allure/"
            build_report=buildurl+"allure/"
            dict = {"issuekey": f"{jirakey}", "project": f"{prjectname}", "result": "success"}
            ATFPlatForm.runDeploy("AutoTest-Result", dict)
            _desc=f'总用例数：100  \\r\\n  失败用例数：10  \\r\\n ' \
                  f'通过用例数：90  \\r\\n 构建详情： {buildurl} \\r\\n 执行结果：{build_report}'
            logger.info(f"备注信息：\n {_desc}")
            JiraPlatForm.setJiraComment(jirakey, _desc)
            JiraPlatForm.setJiraFlowStatus(jirakey, "2551")




if __name__ == '__main__':
    DataBus.set_key("env","test")
    print(ATFPlugin.db_ops('CESNDS',"update tb_send_message s set s.receive_name = '0' , s.receive_telephone = '0' where s.sm_type = 'MajorBookingGroundMuc'").text)

