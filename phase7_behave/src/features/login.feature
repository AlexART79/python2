Feature: Login

Scenario: Login with correct credentials
    Given open login page in browser
     When user logging in using 'Alexander_Artemov', 'Alexander_Artemov'
     Then user should be successfully logged in