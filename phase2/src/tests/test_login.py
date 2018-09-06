import pytest
import requests
from ..jira import Jira
from .fixtures.login_info import AuthInfo


class TestLogin:
    @pytest.mark.parametrize("login_data", [AuthInfo("test", "test", 403),
                                            AuthInfo("Alexander_Artemov", "test", 401),
                                            AuthInfo("Alexander_Artemov", "Alexander_Artemov", 200)])
    def test_login(self, login_data):
        jira = Jira()

        r = requests.post(jira.auth_endpoint,
                          json=login_data.get_json(),
                          headers={"Content-Type": "application/json"})

        assert r.status_code == login_data.exp_status