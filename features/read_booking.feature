Feature: Read a specific booking
    Scenario: Read a specific booking with an id
        Given the user creates a booking under my name
        When the user wants to "read" the created booking
        When the user is finished inputting data
        Then the output should contain the created booking
        Then the output should not contain "Booking id does not exist"

    Scenario: Read a fake booking
        When the user enters "read"
        And the user enters "0"
        When the user is finished inputting data
        Then the output should contain "Booking id does not exist"
