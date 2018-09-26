Feature: Login

Background:
    Given open login page in browser


Scenario: Login with correct credentials
     When user logging in using "Alexander_Artemov", "Alexander_Artemov"
     Then user should be successfully logged in


Scenario Outline: Login Incorrect
     When user logging in using "<username>", "<password>"
     Then user should get a login error message

    Examples:
      | username          | password |
      | alex_art          | test     |
      | Alexander_Artemov | N/A      |
      | N/A               | test     |

