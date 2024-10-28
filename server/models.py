from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base

# joinning table for many-to-many relationship
user_application_association = Table(
    'user_application', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.user_id'), primary_key=True),
    Column('application_id', Integer, ForeignKey('application.application_id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    _password_hash =Column(String(200), nullable= False)
    email = Column(String(200), nullable=False)
    fullname = Column(String(100), nullable=False)
    role = Column(String(50), nullable= False)
    department = Column(String(50), nullable=False)

    applicaton = relationship('Application', back_populates='users')

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.name}, fullname={self.fullname}), role={self.role}, department={self.department}"
    
class Applicaton(Base):
    __talbename__ = 'application'

    application_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    create_date = Column(Date, nullable=False, default= Date.now()),
    application_status = Column(String(50), nullable=False, default="SUBMITTED")

    user = relationship('User', back_populates='applications')

    def __repr__(self):
        return f"Application(application_id={self.application_id}, user_id={self.user_id}, create_date={self.create_date}, application_status={self.application_status})"