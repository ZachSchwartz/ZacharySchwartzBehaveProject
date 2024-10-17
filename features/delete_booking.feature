Feature: Delete a booking, or gracefully fail if impossible
    Scenario: Delete a created booking
        Given the user creates a booking under my name
        When the user wants to "delete" the created booking
        When the user is finished inputting data
        Then the output should contain "Booking deleted"

    Scenario: Delete a fake booking
        Given the user creates a booking under my name
        When the user wants to "delete" the created booking
        When the user wants to "delete" the created booking
        When the user is finished inputting data
        Then the output should contain "Booking id does not exist"