import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from faker import Faker
import random as rc
import os
import sys

fake = Faker()
engine = create_engine('sqlite:///./loan_application.db')

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_dir)

from server.models import User, UserApplication

sql_file_path = os.path.join(current_dir, "LoanDB.sql")


# Read the SQL file and execute the sql script to create database and tables
with engine.connect() as conn:
    with open(sql_file_path, "r") as sql_file:
        sql_script = sql_file.read()

    sql_statements = sql_script.strip().split(';')

    for statement in sql_statements:
        if statement.strip():
            conn.execute(text(statement))

# load data into pandas dataframe
df = pd.read_csv(os.path.join(current_dir,'loan_application.csv'))

# add dataframe data to database application table
with engine.begin() as conn:
    df.to_sql('application', con=conn, if_exists='append', index=False)

# create fake user data
def create_fake_users():
    users = []
    emails = []
    roles = ['Loan officer', 'Underwriter', 'Loan processor', ' Credit administrator']
    for _ in range(10):
        email = fake.email()
        while email in emails:
            emails = fake.email()
        emails.append(email)
        fullname = fake.name()
        user = User(email=email, fullname=fullname, role=rc.choice(roles), department = 'Loan')
        with Session(engine) as session:
            session.add(user)
            session.commit
        user.password_hash= user.email.split('@', 1)[0] + 'password'
        users.append(user)
    return users

# create fake user_application data
def create_fake_user_application():
    pair_nums = set()
    user_applications = []
    while len(pair_nums) < 50:
        num1 = rc.randint(1, 10)
        num2 = rc.randint(1, 252000)
        pair_nums.add((num1, num2))
    for user_id, application_id in pair_nums:
        user_application = UserApplication(user_id = user_id, application_id = application_id)
        user_applications.append(user_application)
    
    # print(user_applications)
    return user_applications

    

# add fake user data to database user table
with Session(engine) as session:
    session.add_all(create_fake_users())
    session.commit()
    session.add_all(create_fake_user_application())
    session.commit()

print("Database and tables created successfully.")


