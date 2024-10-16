""""The goal of this project is to allow the user to easily interface with the restful-booker api"""

from urllib.parse import urlencode
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


def create_token():
    """Creates a new auth token to use for access to the UPDATE and DELETE booking"""
    url = "https://restful-booker.herokuapp.com/auth"
    headers = {"Content-Type": "application/json"}
    data = {"username": "admin", "password": "password123"}
    response = requests.post(url, json=data, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json().get("token")


def create_booking(booking: dict):
    """Creates new booking"""
    url = "https://restful-booker.herokuapp.com/booking"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(url, json=booking, headers=headers, timeout=10)
    response.raise_for_status()
    print("Booking Created: ")
    print(response.json())


def read_booking(booking_id):
    """Reads the contents of a pre-existing booking"""
    url = f"https://restful-booker.herokuapp.com/booking/{str(booking_id)}"
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Here is booking {booking_id}")
        print(response.json())
        return response.json()
    except requests.exceptions.HTTPError:
        print("Booking id does not exist")


def update_booking(booking_id, token, booking: dict):
    """Updates a pre-existing booking with a new booking"""
    url = f"https://restful-booker.herokuapp.com/booking/{str(booking_id)}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={token}",
    }
    response = requests.put(url, json=booking, headers=headers, timeout=10)
    response.raise_for_status()
    print(f"Booking {booking_id} updated")
    print(response.json())


def delete_booking(booking_id, token):
    """Deletes a booking"""
    url = f"https://restful-booker.herokuapp.com/booking/{str(booking_id)}"
    headers = {"Content-Type": "application/json", "Cookie": f"token={token}"}
    try:
        response = requests.delete(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Booking deleted: {booking_id}")
    except requests.exceptions.HTTPError:
        print("Booking id does not exist")


def get_bookings(firstname=None, lastname=None, checkin=None, checkout=None):
    """Gets a list of all booking ids, can be filtered based on names and checkin/out times"""
    url = "https://restful-booker.herokuapp.com/booking"
    params = {}
    if firstname:
        params["firstname"] = firstname
    if lastname:
        params["lastname"] = lastname
    if checkin:
        params["checkin"] = checkin
    if checkout:
        params["checkout"] = checkout

    query_string = urlencode(params)
    response = requests.get(
        f"{url}?{query_string}" if query_string else url, timeout=10
    )
    print(f"{url}?{query_string}")
    response.raise_for_status()
    print("Here are the requested booking(s): ")
    print(response.json())


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
    firstname = get_input("Please enter the first name ")
    lastname = get_input("Please enter the last name ")
    totalprice = get_input("Please enter the total price paid ", validate_price)
    deposit = get_input(
        "Enter 'true' if they paid their deposit, or anything else if they have not "
    )
    checkin = get_input(
        "Please enter a checkin time following the format (YYYY-MM-DD) ", validate_date
    )
    checkout = get_input(
        "Please enter a checkout time following the format (YYYY-MM-DD) ", validate_date
    )
    additional_needs = get_input("Please enter the if there additional needs ")
    booking = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": int(totalprice),
        "depositpaid": deposit.lower() == "true",
        "bookingdates": {"checkin": checkin, "checkout": checkout},
        "additionalneeds": additional_needs,
    }
    create_booking(booking)


def handle_get_ids():
    """Handles the user side of getting ids"""
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
    get_bookings(firstname, lastname, checkin, checkout)


def handle_read_booking():
    """Handles the user side of reading a booking"""
    id_input = input("Please enter a booking id to read ")
    read_booking(id_input)


def handle_update(token):
    """Handles the user side of updating a booking"""
    id_input = input("Please enter a booking id ")
    booking = read_booking(id_input)
    firstname = get_input(
        f"Enter firstname if you'd like to replace {booking.get("firstname")}, enter nothing to keep original value ",
        old_value=booking.get("firstname"),
    )
    lastname = get_input(
        f"Enter lastname if you'd like to replace {booking.get("lastname")}, enter nothing to keep original value ",
        old_value=booking.get("lastname"),
    )
    totalprice = get_input(
        f"Enter the total price if you'd like to replace {booking.get("totalprice")}, enter nothing to keep original value ",
        validate_price,
        booking.get("totalprice"),
    )
    deposit = get_input(
        f"Enter 'true' if the deposit was paid, and if you'd like to replace {booking.get("depositpaid")}, enter nothing to keep original value ",
        old_value=str(booking.get("depositpaid")),
    )
    checkin = get_input(
        f"Enter checkin if you'd like to replace {booking.get("bookingdates").get("checkin")}, enter nothing to keep original value ",
        validate_date,
        booking.get("bookingdates").get("checkin"),
    )
    checkout = get_input(
        f"Enter checkout if you'd like to replace {booking.get("bookingdates").get("checkout")}, enter nothing to keep original value ",
        validate_date,
        booking.get("bookingdates").get("checkout"),
    )
    additional_needs = get_input(
        f"Enter additional needs if you'd like to replace {booking.get("additionalneeds")}, enter nothing to keep original value ",
        old_value=booking.get("additionalneeds"),
    )
    updated_booking = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": deposit.lower() == "true",
        "bookingdates": {"checkin": checkin, "checkout": checkout},
        "additionalneeds": additional_needs,
    }
    update_booking(id_input, token, updated_booking)


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
