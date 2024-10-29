from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, registry, Mapped, mapped_column, relationship
from datetime import date
import bcrypt

metadata = MetaData()
engine = create_engine('sqlite:///../database/loan_application.db')
type_annotation_map = {
    str: String, int: Integer, date: Date
}

mapper_registry = registry(type_annotation_map=type_annotation_map)
class Base(DeclarativeBase):
    metadata = metadata
    registry = mapper_registry

# joinning table for many-to-many relationship
user_application_association = Table(
    'user_application', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.user_id'), primary_key=True),
    Column('application_id', Integer, ForeignKey('application.application_id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    _password_hash: Mapped[str] =mapped_column(String(200), nullable= False)
    email: Mapped[str] = mapped_column(String(200), nullable=False)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable= False)
    department: Mapped[str] = mapped_column(String(50), nullable=False)

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
        return f"User(user_id={self.user_id}, email={self.email}, fullname={self.fullname}), role={self.role}, department={self.department}"
    
class Applicaton(Base):
    __tablename__ = 'application'

    application_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    create_date = mapped_column(Date, nullable=False, default= func.now())
    application_status: Mapped[str] = mapped_column(String(50), nullable=False, default="SUBMITTED")

    users = relationship('User', secondary=user_application_association, back_populates='applications')

    def __repr__(self):
        return f"Application(application_id={self.application_id}, create_date={self.create_date}, application_status={self.application_status})"
    
Base.metadata.create_all(engine)