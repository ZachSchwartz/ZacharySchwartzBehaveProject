"""Handles the requests to the restful booker api"""

from urllib.parse import urlencode
import requests

URL = "https://restful-booker.herokuapp.com/booking"
CONTENT_HEADER = {"Content-Type": "application/json"}
ACCEPT_HEADER = {"Accept": "application/json"}
COMBINED_HEADER = {**CONTENT_HEADER, **ACCEPT_HEADER}


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


def get_bookings(booking: dict):
    """Gets a list of all booking ids, can be filtered based on names and checkin/out times"""
    booking_filtered = {k: v for k, v in booking.items() if v}
    query_string = urlencode(booking_filtered)
    return requests.get(f"{URL}?{query_string}" if query_string else URL, timeout=10)


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
