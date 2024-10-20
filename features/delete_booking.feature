Feature: Delete a booking, or gracefully fail if impossible
    Scenario: Delete a created booking
        Given the user creates a booking under my name
        When the user wants to "delete" the created booking
        When the user is finished inputting data
        Then the output should contain "Booking deleted"
        Then the output should not contain "Booking id does not exist"

    Scenario: Delete a fake booking
        When the user enters "delete"
        And the user enters "0"
        When the user is finished inputting data
        Then the output should not contain "Booking deleted"
        Then the output should contain "Booking id does not exist"