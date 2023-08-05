from common.common.api_driver import APIDriver
from common.data.handle_common import extractor, get_system_key, set_system_key

from common.common.constant import Constant
from requests.auth import HTTPBasicAuth


class JiraPlatForm(object):

    @classmethod
    def getJiraIssueInfo(self, jira_no):
        return APIDriver.http_request(url=f"{Constant.JIRA_URL}/rest/api/2/issue/{jira_no}",method='get',
                                        _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME),get_system_key(Constant.JIRA_PASSWORD)),
                                                            _log=False)
    @classmethod
    def getJiraIssueSummer(self, jira_no):
        try:
            if jira_no.find("http://") != -1:
                jira_no = jira_no.split("/")[-1]
            _summary = extractor(self.getJiraIssueInfo(jira_no).json(), "$.fields.summary")
            if str(_summary).find("$") != -1:
                _summary = None
                _link = f'{Constant.JIRA_URL}/browse/{jira_no}'
            else:
                _link = f'{Constant.JIRA_URL}/browse/{jira_no}'
        except Exception as e:
            _summary = None
            _link = f'{Constant.JIRA_URL}/browse/{jira_no}'
        return  _summary, _link, jira_no



