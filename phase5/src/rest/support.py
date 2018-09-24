# class to store issue data for tests
class IssueInfo:
    def __init__(self, project=None, summary=None, description=None, type=None, expected=None):
        self.project = {"key": project} if project is not None else False
        self.summary = summary
        self.description = description
        self.type = {"name": type} if type is not None else False

        self.expected = expected

    def get_json(self):
        dict_asd = {"fields": {}}
        if self.project:
            dict_asd["fields"]['project'] = self.project

        if self.summary:
            dict_asd["fields"]['summary'] = self.summary
        if self.description:
            dict_asd["fields"]['description'] = self.description
        if self.type:
            dict_asd["fields"]['issuetype'] = self.type

        return dict_asd


class AuthInfo:
    def __init__(self, login, password, status=None):
        self.login = login
        self.password = password
        self.exp_status = status

    def get_json(self):
        return {"username": self.login, "password": self.password}