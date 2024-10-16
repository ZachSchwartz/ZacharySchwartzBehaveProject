Feature: Read Booking IDs
  Scenario: User reads all booking IDs
    When the user enters "get ids"
    When the user enters nothing for "3" other inputs
    When the user is finished inputting data
    Then the output should contain "Here are the requested booking(s):"
    Then the output should contain "[{'bookingid':"
  
  Scenario: User queries a specific booking with a first and last name
    Given the user creates a booking under my name
    When the user enters "get ids"
    And the user enters "Zach"
    And the user enters "Schwartz"
    When the user enters nothing for "1" other inputs
    When the user is finished inputting data
    Then the output should contain "Here are the requested booking(s):"
    Then the user should be looking at the correct booking entry

Scenario: User queries a specific booking with a first name
    Given the user creates a booking under my name
    When the user enters "get ids"
    And the user enters "Zach"
    When the user enters nothing for "2" other inputs
    When the user is finished inputting data
    Then the output should contain "Here are the requested booking(s):"
    Then the user should be looking at the correct booking entry

  Scenario: User queries a specific id with a checkout date
    Given the user creates a booking under my name
    When the user enters "get ids"
    When the user enters nothing for "2" other inputs
    When the user enters "2020-02-02"
    When the user is finished inputting data
    Then the output should contain "Here are the requested booking(s):"
    Then the user should be looking at the correct booking entry

  Scenario: User queries a specific booking with all arguments
    Given the user creates a booking under my name
    When the user enters "get ids"
    And the user enters "Zach"
    And the user enters "Schwartz"
    And the user enters "2020-01-01"
    When the user is finished inputting data
    Then the output should contain "Here are the requested booking(s):"
    Then the user should be looking at the correct booking entry