[![CircleCI](https://circleci.com/gh/AlexART79/python2/tree/phase5.svg?style=svg)](https://circleci.com/gh/AlexART79/python2/tree/phase5)

#Python course: phase 5/6
##Tags
Test suite contains 2 kinds of tests that are marked with appropriate tags:
* UI - selenium UI tests
* API - API tests

There are also marks on the tests that allow users to run particular categories:
* apitest
* uitest 

###Usage
<code>pytest -m \<category\></code>

##Report
To collect allure test results after test run, run the tests with the <b>--alluredir=test_results"</b> argument:
<br /><code>pytest -m \<category\> --alluredir=path_to_results</code>

After that you'll be able to generate report using allure cmd-line:
<br /><code>allure generate path_to_results -o path_to_report</code>

And open report by using
<br /><code>allure open path_to_report</code>