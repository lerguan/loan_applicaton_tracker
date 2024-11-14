# Loan Application Progress Tracker

## Introduction

The CLI application helps loan department employee to assign, track, modify the loan application progress.

- The `database` folder contains `createDB.py` to create the database and insert data. The dataset`loan_approval_dataset.json` is obtained from kaggle. The database includes three tables: `application`, `user`, `user_application`.
- The `server` folder contains a python application for the back-end.

## Setup

### Generating Database

Change into the `database` directory and create database and populate application data, as well as some dummy user accounts:

```console
cd server
python createDB.py
```

## Use

Change into the root directory and run app:

```console
python app.py
```

A main menu asks the user to register/login account. The dummy user account is setup for test purpose. For example, a test user may use email address `lsingh@example.org` and password `lsinghpassword` to login

After user login, the application manager menu gives user 6 options with

1. Assign New Application to Me
2. Search for Application
3. Update Application Status
4. Check Application Status
5. Display Applications Assigned to Me
6. Logout

- `Assign New Application to Me` : Users can assign new loan application to themselves
- `Search for Application` : Users can search for specific loan application with application_id to see the detail of the application in database
- `Update Application Status` : Users can update specific loan application status
- `Check Application Status` : Users can check specific loan application status
- `Display Applications Assigned to Me` : Users can display all the loan application assigned to themselves.
- `Logout` : Users logout their account and back to the main menu.
