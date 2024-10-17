Feature: Read a specific booking
    Scenario: User reads a specific booking with an id
        Given the user creates a booking under my name
        When the user wants to "read" the created booking
        When the user is finished inputting data
        Then the output should contain the created booking

    Scenario: User reads a fake booking
        When the user enters "read"
        And the user enters "0"
        When the user is finished inputting data
        Then the output should contain "Booking id does not exist"
