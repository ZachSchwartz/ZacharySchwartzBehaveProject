""""The goal of this project is to allow the user to easily interface with the restful-booker api"""

from URLlib.parse import URLencode
from datetime import datetime
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
CREATE_REQUEST = "Please enter the {}"
BOOKING_ID_NAME_REQUEST = "Enter {} if you'd like to filter by that kind of name, enter nothing to skip "
BOOKING_ID_DATE_REQUEST = "Enter {} date (YYYY-MM-DD) to filter by that date, enter nothing to skip "
UPDATE_REQUEST = "Please enter the {} if you'd like to replace {}, enter nothing to keep original value "

ATTRIBUTES = {
    "firstname": "first name ",
    "lastname": "last name ",
    "totalprice": "total price paid ",
    "depositpaid": "deposit status, type 'true' or anything else for false",
    "checkin": "checkin date ",
    "checkout": "checkout date ",
    "additionalneeds": "additional needs ",
}


def create_token():
    """Creates a new auth token to use for access to the UPDATE and DELETE booking"""
    token_url = "https://restful-booker.herokuapp.com/auth"
    headers = {"Content-Type": "application/json"}
    data = {"username": "admin", "password": "password123"}
    return requests.post(token_url, json=data, headers=headers, timeout=10)


def create_booking(booking: dict):
    """Creates new booking"""
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    return requests.post(URL, json=booking, headers=headers, timeout=10)


def read_booking(booking_id):
    """Reads the contents of a pre-existing booking"""
    headers = {"Accept": "application/json"}
    return requests.get(URL + f"/{str(booking_id)}", headers=headers, timeout=10)


def update_booking(booking_id, token, booking: dict):
    """Updates a pre-existing booking with a new booking"""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}",
    }
    return requests.put(
        URL + f"/{str(booking_id)}", json=booking, headers=headers, timeout=10
    )


def delete_booking(booking_id, token):
    """Deletes a booking"""
    headers = {"Content-Type": "application/json", "Cookie": f"token={token}"}
    return requests.delete(URL + f"/{str(booking_id)}", headers=headers, timeout=10)


def get_bookings(firstname=None, lastname=None, checkin=None, checkout=None):
    """Gets a list of all booking ids, can be filtered based on names and checkin/out times"""
    params = {}
    if firstname:
        params["firstname"] = firstname
    if lastname:
        params["lastname"] = lastname
    if checkin:
        params["checkin"] = checkin
    if checkout:
        params["checkout"] = checkout

    query_string = URLencode(params)
    return requests.get(f"{URL}?{query_string}" if query_string else URL, timeout=10)


def get_input(prompt, validator=None, old_value=None):
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
        print("Did not receive valid date from user")
        return False


def validate_price(input_string):
    """Validates receiving a proper number from user"""
    try:
        price = int(input_string)
        return price >= 0
    except ValueError:
        print("Did not receive valid, positive whole number from user")
        return False


def handle_create_booking():
    """Handles the user side of creating a booking entry"""
    booking = {}
    for attribute, message in ATTRIBUTES:
        if "total price paid " == attribute:
            booking[attribute] = get_input(
                CREATE_REQUEST.format(message), validate_price
            )
        elif "date" in message:
            booking[attribute] = get_input(CREATE_REQUEST.format(message), validate_date)
        else:
            booking[attribute] = get_input(CREATE_REQUEST.format(message))
    print(create_booking(booking).json())


def handle_get_ids():
    """Handles the user side of getting ids"""
    booking = {}
    for attribute in ATTRIBUTES:
        if "name" in attribute:
            booking[attribute] = get_input(
                BOOKING_ID_NAME_REQUEST.format(attribute)
            )
        elif "date" in attribute:
            booking[attribute] = get_input(BOOKING_ID_DATE_REQUEST.format(attribute), validate_date)
            

    firstname = (
        input(
            "Enter firstname if you'd like to filter by firstname, enter nothing to skip "
        )
        or None
    )
    lastname = (
        input(
            "Enter lastname if you'd like to filter by lastname, enter nothing to skip "
        )
        or None
    )
    checkin = (
        input("Enter check-in date (YYYY-MM-DD) to search, enter nothing to skip ")
        or None
    )
    checkout = (
        input("Enter check-out date (YYYY-MM-DD) to search, enter nothing to skip ")
        or None
    )
    print(get_bookings(firstname, lastname, checkin, checkout).json())


def handle_read_booking():
    """Handles the user side of reading a booking"""
    id_input = input("Please enter a booking id to read ")
    read_booking(id_input)


def handle_update(token):
    """Handles the user side of updating a booking"""
    id_input = input("Please enter a booking id ")
    booking = read_booking(id_input)
    booking = {}
    for attribute, message in ATTRIBUTES:
        if "total price paid " == attribute:
            booking[attribute] = get_input(
                UPDATE_REQUEST.format(message, booking.get(attribute)), validate_price
            )
        elif "date" in message:
            booking[attribute] = get_input(UPDATE_REQUEST.format(message, booking.get(attribute)), validate_date)
        else:
            booking[attribute] = get_input(UPDATE_REQUEST.format(message, booking.get(attribute)))
    print(update_booking(id_input, token, booking).json())


def handle_delete(token):
    """Handles the user side of deleting a booking"""
    id_input = input("Please enter a booking id to delete ")
    delete_booking(id_input, token)


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


user_interface()
