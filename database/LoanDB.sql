BEGIN TRANSACTION;

DROP TABLE IF EXISTS user_application;
DROP TABLE IF EXISTS application;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username varchar(50) NOT NULL,
    password_hash varchar(200) NOT NULL,
    email varchar(200) NOT NULL,
    fullname varchar(100) NOT NULL,
    role varchar(50) NOT NULL,
    department varchart(50) NOT NULL,
    CONSTRAINT UQ_username UNIQUE (username)
);

CREATE TABLE application (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    income int NOT NULL,
    age int NOT NULL,
    experience_yrs int,
    marital_status varchar(50) NOT NULL,
    house_ownership varchar(50) NOT NULL,
    car_ownership	varchar(50) NOT NULL,
    profession varchar(200) NOT NULL,
    city varchar(50) NOT NULL,
    state varchar(50) NOT NULL,
    current_job_yrs int,
    current_house_yrs int,
    risk_flag int,
    create_date date NOT NULL DEFAULT CURRENT_DATE,
    application_status varchar(50) NOT NULL DEFAULT "SUBMITTED"
);

CREATE TABLE user_application (
    user_id int NOT NULL,
    application_id int NOT NULL,
    CONSTRAINT PK_user_application PRIMARY KEY(user_id, application_id),
    CONSTRAINT FK_user_application_user FOREIGN KEY(user_id) REFERENCES user(user_id),
    CONSTRAINT FK_user_application_application FOREIGN KEY(application_id) REFERENCES application(application_id)
);

COMMIT TRANSACTION;