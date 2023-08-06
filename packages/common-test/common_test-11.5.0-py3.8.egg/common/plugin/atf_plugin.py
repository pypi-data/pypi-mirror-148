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
        jirakey=get_system_key('jirakey')
        prjectname=get_system_key('prjectname')
        jobName=get_system_key('JOB_NAME')
        jobName_url=jobName+"/allure/"
        JiraPlatForm.setJiraFlowStatus(jirakey, "2551")
        JiraPlatForm.setJiraComment(jirakey, jobName_url)
        dict = {"issuekey": f"{jirakey}", "project": f"{prjectname}", "result": "success"}
        ATFPlatForm.runDeploy("AutoTest-Result", dict)



if __name__ == '__main__':
    DataBus.set_key("env","test")
    print(ATFPlugin.db_ops('CESNDS',"update tb_send_message s set s.receive_name = '0' , s.receive_telephone = '0' where s.sm_type = 'MajorBookingGroundMuc'").text)

