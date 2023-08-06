from common.plat.service_platform import ServicePlatForm
from common.config.config import TEST_TARGET_REPORT_PATH
from common.data.data_process import DataProcess
from common.plugin.data_plugin import DataPlugin
from common.plugin.file_plugin import FilePlugin
from loguru import logger
from common.data.handle_common import get_system_key
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
    def sendResult(self,report_html_path: str = TEST_TARGET_REPORT_PATH):
        if get_system_key('runtype') is not None:
            prjectname=get_system_key('name')
            buildurl=get_system_key('BUILD_URL')
            build_report = buildurl+"allure/"
            _summary=FilePlugin.load_json(f'{report_html_path}/widgets/summary.json')
            _total = DataPlugin.get_data_jpath(_summary,"$.statistic.total")
            _passed= DataPlugin.get_data_jpath(_summary,"$.statistic.passed")
            _failed = DataPlugin.get_data_jpath(_summary, "$.statistic.failed")
            _start = DataProcess.getDate(int(str(DataPlugin.get_data_jpath(_summary, "$.time.start")).strip())/1000)
            _stop = DataProcess.getDate(int(str(DataPlugin.get_data_jpath(_summary, "$.time.stop")).strip())/1000)
            _duration = int(str(DataPlugin.get_data_jpath(_summary, "$.time.duration")).strip())/1000
            if _total > 0 and _passed > 0:
                if get_system_key('toUser') is not None:
                    _list = get_system_key('toUser').split(',')
                    _desc = f'开始时间：{_start}  \n  结束时间：{_stop}  \n ' \
                            f'总用例数：{_total}  \n  失败用例数：{_failed}  \n ' \
                            f'通过用例数：{_passed}  \n ' \
                            f'构建时间：{_duration}S  \n ' \
                            f'构建详情： {buildurl} \n 执行结果：{build_report}'
                    logger.info(f"推送消息：\n {_desc}")
                    ServicePlatForm.sendMsg(_desc, _list)
                if get_system_key('issueKey') is not None:
                    jirakey = get_system_key('issueKey')
                    dict = {"issuekey": f"{jirakey}", "project": f"{prjectname}", "result": "success"}
                    ATFPlatForm.runDeploy("AutoTest-Result", dict)
                    _desc = f'开始时间：{_start}  \\\r\\n   结束时间：{_stop}  \\r\\n  ' \
                            f'总用例数：{_total}  \\r\\n   失败用例数：{_failed}  \\r\\n  ' \
                            f'通过用例数：{_passed}  \\r\\n  ' \
                            f'构建时间：{_duration}S  \\r\\n  ' \
                            f'构建详情： {buildurl} \\r\\n  执行结果：{build_report}'
                    logger.info(f"备注信息：\n {_desc}")
                    JiraPlatForm.setJiraComment(jirakey, _desc)
                    JiraPlatForm.setJiraFlowStatus(jirakey, "2551")




if __name__ == '__main__':
    DataBus.set_key("env","test")
