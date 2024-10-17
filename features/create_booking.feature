Feature: Creating a booking
  Scenario: Create a booking
    When the user enters "create"
    And the user enters "Zach"
    And the user enters "Schwartz"
    And the user enters "100"
    And the user enters "false"
    And the user enters "2020-01-01"
    And the user enters "2020-02-02"
    And the user enters "Nothing"
    When the user is finished inputting data
    Then the output should not contain "Did not receive valid number from user"
    Then the output should not contain "Did not receive valid YYYY-MM-DD from user"
    Then the output should contain "Booking Created: "
    Then the output should contain the created booking

  Scenario: Create booking with certain invalid parameters
    When the user enters "create"
    And the user enters "Zach"
    And the user enters "Schwartz"
    And the user enters "not a number"
    And the user enters "100"
    And the user enters "false"
    And the user enters "not a valid date"
    And the user enters "2020-01-01"
    And the user enters "2020-02-02"
    And the user enters "Nothing"
    When the user is finished inputting data
    Then the output should contain "Did not receive valid number from user"
    Then the output should contain "Did not receive valid YYYY-MM-DD from user"
    Then the output should contain "Booking Created: "
    Then the output should contain the created booking
