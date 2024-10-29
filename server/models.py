from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import relationship, sessionmaker
import bcrypt
from database.createDB import engine

Base = declarative_base()
Session = sessionmaker(bind=engine)

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

    applicatons = relationship('Application', secondary=user_application_association, back_populates='users')

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.hashpw(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.checkpw(self._password_hash, password.encode("utf-8"))

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.name}, fullname={self.fullname}), role={self.role}, department={self.department}"
    
class Applicaton(Base):
    __tablename__ = 'application'

    application_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    create_date = Column(Date, nullable=False, default= func.now())
    application_status = Column(String(50), nullable=False, default="SUBMITTED")

    users = relationship('User', secondary=user_application_association, back_populates='applications')

    def __repr__(self):
        return f"Application(application_id={self.application_id}, create_date={self.create_date}, application_status={self.application_status})"
    

def init_db():
    Base.metadata.createAll(engine)