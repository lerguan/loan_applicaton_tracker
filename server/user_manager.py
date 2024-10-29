from server.models import Session, User
from sqlalchemy.exc import IntegrityError

class UserManager:
    def __init__(self):
        self.session = Session()

    def register_user(self, username, password, email, fullname, role, department):
        if self.session.query(User).filter_by(username=username).first():
            return 'Username already exists, please choose another one!'
        
        new_user = User(username=username, email=email, fullname=fullname, role=role, department=department)
        new_user.password_hash = password
        
        try:
            self.session.add(new_user)
            self.session.commit()

            return f'User {username} registered!'
        except IntegrityError:
            self.session.rollback()
            return 'error: 422 unprocessable entity'

    
    def login_user(self, username, password):
        user = self.session.query(User).filter_by(username=username).first()

        if user and user.authenticate(password):
            self.session.add(user)
            self.session.commit()

            return 'Welcome Back!'
        
        return 'Invalid username and/or passoword!'