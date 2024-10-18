""""The goal of this project is to allow the user to easily interface with the restful-booker api"""

from datetime import datetime
import requests
import booker_requests

WELCOME_STRING = """Please enter one of the options
create
get ids
read
update
delete
exit
"""

CREATE_REQUEST = "Please enter the {} "
BOOKING_ID_REQUEST = "Please enter a booking id "
BOOKING_ID_NAME_REQUEST = "Please enter the {} if you'd like to filter by that kind of name, enter nothing to skip "
BOOKING_ID_DATE_REQUEST = "Please enter the {} date (YYYY-MM-DD) to filter by that date, enter nothing to skip "
UPDATE_REQUEST = (
    "Please enter the {} to replace {}, enter nothing to keep original value "
)
INVALID_ID = "Booking id does not exist"
ATTRIBUTES = {
    "firstname": "first name",
    "lastname": "last name",
    "totalprice": "total price paid",
    "depositpaid": "deposit status, type 'true' or anything else for false",
    "checkin": "checkin date",
    "checkout": "checkout date",
    "additionalneeds": "additional needs",
}


def validate_date(input_string):
    """Validates receiving a proper date from user"""
    try:
        datetime.strptime(input_string, "%Y-%m-%d")
        return True
    except ValueError:
        print("Did not receive valid YYYY-MM-DD from user")
        return False


def validate_price(input_string):
    """Validates receiving a proper number from user"""
    try:
        price = int(input_string)
        return price >= 0
    except ValueError:
        print("Did not receive valid number from user")
        return False


VALIDATORS = {
    "totalprice": validate_price,
    "depositpaid": None,
    "checkin": validate_date,
    "checkout": validate_date,
}


def get_input(prompt, validator=None, old_value=None):
    """Handles getting input from the user for more complex inputs"""
    while True:
        user_input = input(prompt)
        if user_input == "" and old_value is not None:
            return old_value
        if validator is None or validator(user_input):
            return user_input


def update_attribute(message, validator, old_value=None):
    """Helper function to update a booking attribute"""
    if old_value:
        new_value = get_input(
            UPDATE_REQUEST.format(message, old_value),
            validator,
            old_value,
        )
    else:
        new_value = get_input(
            CREATE_REQUEST.format(message),
            validator,
        )

    if "deposit" in message:
        return str(new_value).lower() == "true"

    return new_value


def handle_response(response):
    """Catch errors for responses that involve a booking id"""
    try:
        if response.status_code in {404, 405}:
            response.raise_for_status()
        return response
    except requests.exceptions.HTTPError:
        print(INVALID_ID)
        return None


def handle_create_booking():
    """Handles the user side of creating a booking entry"""
    booking = {"bookingdates": {}}
    for attribute, message in ATTRIBUTES.items():
        validator = VALIDATORS.get(attribute, None)
        if "date" in message:
            booking["bookingdates"][attribute] = update_attribute(message, validator)
            continue

        booking[attribute] = update_attribute(message, validator)

    print("Booking Created: ")
    print(booker_requests.create_booking(booking).json())


def handle_get_ids():
    """Handles the user side of getting ids"""
    booking = {}
    for attribute in ATTRIBUTES:
        if "name" in attribute:
            booking[attribute] = input(BOOKING_ID_NAME_REQUEST.format(attribute))
        elif "checkout" in attribute:
            booking[attribute] = input(BOOKING_ID_DATE_REQUEST.format(attribute))

    print("Here are the requested booking(s): ")
    print(booker_requests.get_bookings(booking).json())


def handle_read_booking():
    """Handles the user side of reading a booking"""
    id_input = input(BOOKING_ID_REQUEST)
    request = handle_response(booker_requests.read_booking(id_input))
    if request:
        print("Here is the requested booking: ")
        print(request.json())


def update_booking_attributes(booking):
    """Updates a booking based on user input"""
    for attribute, message in ATTRIBUTES.items():
        validator = VALIDATORS.get(attribute, None)
        if "date" in message:
            booking["bookingdates"][attribute] = update_attribute(
                message, validator, booking["bookingdates"][attribute]
            )
            continue

        old_value = booking.get(attribute)
        booking[attribute] = update_attribute(message, validator, old_value)

    return booking


def handle_update(token):
    """Handles the user side of updating a booking"""
    id_input = input(BOOKING_ID_REQUEST)
    booking_response = handle_response(booker_requests.read_booking(id_input))
    if booking_response is None:
        return None

    old_booking = booking_response.json()
    print(old_booking)
    new_booking = update_booking_attributes(old_booking)
    print(booker_requests.update_booking(id_input, token, new_booking).json())


def handle_delete(token):
    """Handles the user side of deleting a booking"""
    id_input = input(BOOKING_ID_REQUEST)
    request = handle_response(booker_requests.delete_booking(id_input, token))
    if request:
        print("Booking deleted")


def user_interface():
    """Handles the overall user experience"""
    print("Welcome to Restful Booker!")
    token = booker_requests.create_token()
    while True:
        user_input = input(WELCOME_STRING).lower()
        if user_input == "create":
            handle_create_booking()
        elif user_input == "get ids":
            handle_get_ids()
        elif user_input == "read":
            handle_read_booking()
        elif user_input == "update":
            handle_update(token)
        elif user_input == "delete":
            handle_delete(token)
        elif user_input == "exit":
            break
        else:
            print("I didn't understand that command, please try again\n")


if __name__ == "__main__":
    user_interface()
