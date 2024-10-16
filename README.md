# Zachary Schwartz Behave Project

This project provides a command-line interface for managing hotel bookings through an API. It includes functionality for creating, reading, updating, and deleting bookings, as well as retrieving a list of booking IDs.

## Installation
To set up the project, follow these steps:

Clone the repository:
```
git clone https://github.com/yourusername/ZachSchwartzBehaveProject.git
cd ZachSchwartzBehaveProject
```
Create a virtual enironment, and install required dependencies:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Install the required dependencies:
```
pip install behave requests
```

## Features

1. Create a new booking

2. Read details of an existing booking

3. Update an existing booking

4. Delete a booking

5. Get a list of all booking IDs

When creating or updating a booking, you'll be asked to provide the following information:

1. First name

2. Last name

3. Total price of the booking

4. Whether the deposit has been paid

5. Check-in date (YYYY-MM-DD format)

6. Check-out date (YYYY-MM-DD format)

7. Additional needs from the booker

## Usage
To run the main program:
```
python booker_ui.py
```
Once the program is running, you'll be prompted to enter commands to interact with the API.

## Running Tests
To run the Behave tests:
```
python -m behave
```
## Project Structure
```
│ZachSchwartzBehaveProject/
├── booker_ui.py          # Main program file
├── features/             # Behave test features
│   ├── steps/            # Step definitions for Behave tests
│   └── environment.py    # Behave environment setup
├── requirements.txt      # Project dependencies
└── README.md             # This file```