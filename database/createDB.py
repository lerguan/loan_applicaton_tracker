import pandas as pd
from sqlalchemy import create_engine, text
import os

engine = create_engine('sqlite:///./loan_application.db')

current_dir = os.path.dirname(os.path.abspath(__file__))
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

# add dataframe data to database table
with engine.begin() as conn:
    df.to_sql('application', con=conn, if_exists='append', index=False)

print("Database and tables created successfully from SQL file.")


