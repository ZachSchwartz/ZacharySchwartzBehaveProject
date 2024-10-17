Feature: Update some or all parts of a booking
    Scenario: Update only 1 part of a booking
        Given the user creates a booking under my name
        When the user wants to "update" the created booking
        When the user enters "Gelber"
        When the user enters nothing for "6" other inputs
        When the user is finished inputting data
        Then the output should contain the once updated booking
        Then the output should not contain "Booking id does not exist"

    Scenario: Update all parts of a booking
        Given the user creates a booking under my name
        When the user wants to "update" the created booking
        When the user enters "Gelber"
        When the user enters "Group"
        When the user enters "2"
        When the user enters "True"
        When the user enters "2021-02-02"
        When the user enters "2021-03-03"
        When the user enters "Gelber"
        When the user is finished inputting data
        Then the output should contain the fully updated booking
        Then the output should not contain "Booking id does not exist"

    Scenario: Update a fake booking
        When the user enters "update"
        And the user enters "0"
        When the user is finished inputting data
        Then the output should contain "Booking id does not exist"