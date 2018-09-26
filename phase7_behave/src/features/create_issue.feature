Feature: Create Issue


Background:
    Given open login page in browser
     When user logging in using "Alexander_Artemov", "Alexander_Artemov"
     Then user should be successfully logged in


Scenario: Create Issue Positive
     When user added new issue with the parameters
      | project               | summary            | type | description        | priority |
      | AQAPython (AQAPYTHON) | AlexART - Test Bug | Bug  | this is a test Bug | Low      |
     Then issue should be successfully created


Scenario Outline: Create Issue Negative
     When user opened Create Issue dialog
      And user selected propject '<project>' from the list
      And user selected issue type '<issue_type>' from the list
      And user set summary '<summary>'
      And user set description '<description>'
      And user selected priority '<priority>' from the list
      And user press Create button
     Then user should see error message

  Examples:
      | project               | summary       | issue_type | description          | priority |
      | AQAPython (AQAPYTHON) | N/A           | Bug        | this is a test Bug   | Low      |
      | AQAPython (AQAPYTHON) | ['test '*100] | Story      | this is a test Story | Medium   |
