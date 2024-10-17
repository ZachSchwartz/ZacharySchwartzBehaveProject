""""The goal of this project is to allow the user to easily interface with the restful-booker api"""

from datetime import datetime
from urllib.parse import urlencode
import requests

WELCOME_STRING = """Please enter one of the options
create
get ids
read
update
delete
exit
"""
URL = "https://restful-booker.herokuapp.com/booking"
CREATE_REQUEST = "Please enter the {} "
BOOKING_ID_REQUEST = "Please enter a booking id "
BOOKING_ID_NAME_REQUEST = "Please enter the {} if you'd like to filter by that kind of name, enter nothing to skip "
BOOKING_ID_DATE_REQUEST = "Please enter the {} date (YYYY-MM-DD) to filter by that date, enter nothing to skip "
UPDATE_REQUEST = (
    "Please enter the {} to replace {}, enter nothing to keep original value "
)
CONTENT_HEADER = {"Content-Type": "application/json"}
ACCEPT_HEADER = {"Accept": "application/json"}
COMBINED_HEADER = {**CONTENT_HEADER, **ACCEPT_HEADER}
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


def create_token():
    """Creates a new auth token to use for access to the UPDATE and DELETE booking"""
    token_url = "https://restful-booker.herokuapp.com/auth"
    data = {"username": "admin", "password": "password123"}
    return (
        requests.post(token_url, json=data, headers=CONTENT_HEADER, timeout=10)
        .json()
        .get("token")
    )


def create_booking(booking: dict):
    """Creates new booking"""
    return requests.post(URL, json=booking, headers=COMBINED_HEADER, timeout=10)


def read_booking(booking_id):
    """Reads the contents of a pre-existing booking"""
    return requests.get(URL + f"/{str(booking_id)}", headers=ACCEPT_HEADER, timeout=10)


def update_booking(booking_id, token, booking: dict):
    """Updates a pre-existing booking with a new booking"""
    header = {**COMBINED_HEADER, "Cookie": f"token={token}"}
    return requests.put(
        URL + f"/{str(booking_id)}", json=booking, headers=header, timeout=10
    )


def delete_booking(booking_id, token):
    """Deletes a booking"""
    header = {**CONTENT_HEADER, "Cookie": f"token={token}"}
    return requests.delete(URL + f"/{str(booking_id)}", headers=header, timeout=10)


def get_bookings(booking: dict):
    """Gets a list of all booking ids, can be filtered based on names and checkin/out times"""
    booking_filtered = {k: v for k, v in booking.items() if v}
    query_string = urlencode(booking_filtered)
    return requests.get(f"{URL}?{query_string}" if query_string else URL, timeout=10)


def get_input(prompt, validator=None, old_value=""):
    """Handles getting input from the user for more complex inputs"""
    while True:
        user_input = input(prompt)
        if user_input == "" and old_value is not None:
            return old_value
        if validator is None or validator(user_input):
            return user_input


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
        if "totalprice" == attribute:
            booking[attribute] = get_input(
                CREATE_REQUEST.format(message), validate_price
            )
        elif "date" in message:
            booking["bookingdates"][attribute] = get_input(
                CREATE_REQUEST.format(message), validate_date
            )
        elif "depositpaid" == attribute:
            booking[attribute] = (
                get_input(CREATE_REQUEST.format(message)).lower() == "true"
            )
        else:
            booking[attribute] = get_input(CREATE_REQUEST.format(message))
    print("Booking Created: ")
    print(create_booking(booking).json())


def handle_get_ids():
    """Handles the user side of getting ids"""
    booking = {}
    for attribute in ATTRIBUTES:
        if "name" in attribute:
            booking[attribute] = input(BOOKING_ID_NAME_REQUEST.format(attribute))
        elif "checkout" in attribute:
            booking[attribute] = input(BOOKING_ID_DATE_REQUEST.format(attribute))
    print("Here are the requested booking(s): ")
    print(get_bookings(booking).json())


def handle_read_booking():
    """Handles the user side of reading a booking"""
    id_input = input(BOOKING_ID_REQUEST)
    request = handle_response(read_booking(id_input))
    if request:
        print(request.json())


def handle_update(token):
    """Handles the user side of updating a booking"""
    id_input = input(BOOKING_ID_REQUEST)
    booking = handle_response(read_booking(id_input))
    if booking is None:
        return None
    booking = booking.json()
    print(booking)
    for attribute, message in ATTRIBUTES.items():
        if "date" in message:
            old_attribute = booking["bookingdates"][attribute]
            booking["bookingdates"][attribute] = get_input(
                UPDATE_REQUEST.format(message, old_attribute),
                validate_date,
                old_attribute,
            )
            continue
        old_attribute = booking[attribute]

        if "totalprice" == attribute:
            booking[attribute] = get_input(
                UPDATE_REQUEST.format(message, old_attribute),
                validate_price,
                old_attribute,
            )
        elif "depositpaid" == attribute:
            booking[attribute] = (
                str(
                    get_input(
                        UPDATE_REQUEST.format(message, old_attribute),
                        old_value=old_attribute,
                    )
                ).lower()
                == "true"
            )
        else:
            booking[attribute] = get_input(
                UPDATE_REQUEST.format(message, old_attribute), old_value=old_attribute
            )
    print(update_booking(id_input, token, booking).json())


def handle_delete(token):
    """Handles the user side of deleting a booking"""
    id_input = input(BOOKING_ID_REQUEST)
    request = handle_response(delete_booking(id_input, token))
    if request:
        print("Booking deleted")


def user_interface():
    """Handles the overall user experience"""
    print("Welcome to Restful Booker!")
    token = create_token()
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
