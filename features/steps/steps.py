"""This file holds the code for the .feature files of the projects automated testing"""

from unittest.mock import patch
import io
import sys
import re
from behave import when, then, given
from booker_ui import user_interface


EXPECTED_BOOKING = """{'firstname': 'Zach', 'lastname': 'Schwartz', 'totalprice': 100, 'depositpaid': False, 'bookingdates': {'checkin': '2020-01-01', 'checkout': '2020-02-02'}, 'additionalneeds': 'Nothing'}"""
ONCE_UPDATED_BOOKING = """{'firstname': 'Gelber', 'lastname': 'Schwartz', 'totalprice': 100, 'depositpaid': False, 'bookingdates': {'checkin': '2020-01-01', 'checkout': '2020-02-02'}, 'additionalneeds': 'Nothing'}"""
FULLY_UPDATED_BOOKING = """{'firstname': 'Gelber', 'lastname': 'Group', 'totalprice': 2, 'depositpaid': True, 'bookingdates': {'checkin': '2021-02-02', 'checkout': '2021-03-03'}, 'additionalneeds': 'Gelber'}"""


@given("the user creates a booking under my name")
def step_user_creates_booking(context):
    """Creates an entry with specific parameters, and resets the test to otherwise start from scratch
    This is used for the tests that require an entry with specific parameters,
    but the functionality of being able to create a test is not the objective of the test.
    """
    context.input.append("create")
    context.input.append("Zach")
    context.input.append("Schwartz")
    context.input.append("100")
    context.input.append("")
    context.input.append("2020-01-01")
    context.input.append("2020-02-02")
    context.input.append("Nothing")
    step_finished_inputting_data(context)
    pattern = r"'bookingid': (\d+)"
    match = re.search(pattern, context.output)
    context.id = match.group(1)
    context.input = []
    context.output = ""


@when('the user enters "{text}"')
def step_user_enters_text(context, text):
    """Generic text insert into the cli"""
    context.input.append(text)


@when('the user wants to "{text}" the created booking')
def step_user_enters_command_with_booking(context, text):
    """Enters a command, and then the booking id created earlier from step_user_creates_booking"""
    context.input.append(text)
    context.input.append(context.id)


@when('the user enters nothing for "{text}" other inputs')
def step_user_enters_no_text(context, text):
    """Some of the tests require empty entries into the cli,
    but the step_user_enters_text does not accept an empty string, so this function places empty strings
    """
    for i in range(int(text)):
        context.input.append("")


@when("the user is finished inputting data")
def step_finished_inputting_data(context):
    """Runs the program with the previous inputs,
    exits the program, recording all of the outputted text into context.output"""
    context.input.append("exit")
    input_mock = patch("builtins.input", side_effect=context.input)
    stdout_capture = io.StringIO()
    stdout_mock = patch("sys.stdout", new=stdout_capture)
    with input_mock, stdout_mock:
        user_interface()
    context.output = stdout_capture.getvalue()
    sys.stdout = sys.__stdout__
    sys.stdin = sys.__stdin__


@then('the output should contain "{expected_text}"')
def step_output_should_contain(context, expected_text):
    """Generic assert for what output should contain"""
    assert (
        expected_text in context.output
    ), f"Expected '{expected_text}' not found in output"


@then('the output should not contain "{expected_text}"')
def step_output_should_not_contain(context, expected_text):
    """Generic assert for what output should not contain"""
    assert (
        expected_text not in context.output
    ), f"Expected '{expected_text}' not found in output"


@then("the user should be looking at the correct booking entry")
def step_read_booking(context):
    """Asserts sure the program was able to access the created booking from step_user_creates_booking"""
    assert f"{context.id}" in context.output, "Expected to see correct booking id"


@then("the output should contain the created booking")
def step_output_should_contain_created_booking(context):
    """Asserts that the created booking was received by the server"""
    assert EXPECTED_BOOKING in context.output, "Expected text not found in output"


@then("the output should contain the once updated booking")
def step_output_should_contain_once_updated_booking(context):
    """Asserts that the once updated booking was received by the server"""
    assert ONCE_UPDATED_BOOKING in context.output, "Expected text not found in output"


@then("the output should contain the fully updated booking")
def step_output_should_contain_fully_updated_booking(context):
    """Asserts that the completely modified booking was received by the server"""
    assert FULLY_UPDATED_BOOKING in context.output, "Expected text not found in output"
