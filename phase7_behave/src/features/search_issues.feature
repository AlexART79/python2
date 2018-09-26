Feature: Search

Background:
    Given there are some issues in jira
      And open login page in browser
     When user logging in using "Alexander_Artemov", "Alexander_Artemov"
     Then user should be successfully logged in


Scenario Outline: Search Issues
    Given user is on issues search page
     When user input '<jql>' string into search field
      And press Enter key
     Then there should be <result> issues found

  Examples:
      | jql                                              | result |
      | summary~'AA_issue_to_find'                       | 5      |
      | summary~'AA_issue_to_find' AND issuetype = Story | 1      |
      | summary~'AA_issue_to_find' AND issuetype = Epic  | 0      |