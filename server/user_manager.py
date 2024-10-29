from server.models import engine, User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

class UserManager:
    def __init__(self):
        self.session = Session(engine)

    def register_user(self, password, email, fullname, role, department):
        if self.session.query(User).filter_by(email=email).first():
            return 'User already exists!'
        
        new_user = User(email=email, fullname=fullname, role=role, department=department)
        new_user.password_hash = password
        
        try:
            self.session.add(new_user)
            self.session.commit()

            return f'User {email} registered!'
        except IntegrityError:
            self.session.rollback()
            return 'error: 422 unprocessable entity'

    
    def login_user(self, email, password):
        user = self.session.query(User).filter_by(email=email).first()

        if user and user.authenticate(password):
            self.session.add(user)
            self.session.commit()

            return 'Welcome Back!'
        
        return 'Invalid username and/or passoword!'