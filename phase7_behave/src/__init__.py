import sys
import os

home_dir = os.path.expanduser("~")
sys.path.append(os.path.join(home_dir, 'phase7_behave/src'))
sys.path.append("/home/circleci/repo/phase7_behave/src")
sys.path.append("/home/circleci/repo/phase7_behave")

# making absolute references shorter...
from .features.steps.common import transform_parameters
from .pages.pages import GeneralPage, DashboardPage, IssuesSearchPage, LoginPage
from .rest.jira import Jira
from .rest.support import IssueInfo
from .DriverManager import DriverManager

