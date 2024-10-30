from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import create_engine, MetaData, Integer, String, Date, ForeignKey, func, Table, Column
from sqlalchemy.orm import DeclarativeBase, registry, Mapped, mapped_column, relationship
from datetime import date
import bcrypt
import os

metadata = MetaData()
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../loan_application.db')
engine = create_engine(f'sqlite:///{db_path}')
type_annotation_map = {
    str: String(), int: Integer, date: Date
}

mapper_registry = registry(type_annotation_map=type_annotation_map)
class Base(DeclarativeBase):
    metadata = metadata
    registry = mapper_registry

# joinning table for many-to-many relationship
class UserApplication(Base):
    __tablename__ = 'user_application'
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.user_id'), primary_key=True)
    application_id: Mapped[int] = mapped_column(Integer, ForeignKey('application.application_id'), primary_key=True)

class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    _password_hash: Mapped[str] =mapped_column(String(200), nullable= False)
    email: Mapped[str] = mapped_column(String(200), nullable=False)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable= False)
    department: Mapped[str] = mapped_column(String(50), nullable=False)

    # applications = relationship("Application", secondary='user_application', back_populates='users')

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self._password_hash.encode("utf-8"))

    def __repr__(self):
        return f"User(user_id={self.user_id}, email={self.email}, fullname={self.fullname}), role={self.role}, department={self.department}"
    
class Application(Base):
    __tablename__ = 'application'

    application_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    income: Mapped[int] = mapped_column(Integer, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    experience_yrs: Mapped[int] = mapped_column(Integer, nullable=False)
    marital_status: Mapped[str] = mapped_column(String(50), nullable=False)
    house_ownership: Mapped[str] = mapped_column(String(50), nullable=False)
    car_ownership: Mapped[str] = mapped_column(String(50), nullable=False)
    profession: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(50))
    state: Mapped[str] = mapped_column(String(50))
    current_job_yrs: Mapped[int] = mapped_column(Integer)
    current_house_yrs: Mapped[int] = mapped_column(Integer)
    risk_flag: Mapped[int] = mapped_column(Integer)
    create_date: Mapped[date] = mapped_column(Date, nullable=False, default= func.now())
    application_status: Mapped[str] = mapped_column(String(50), nullable=False, default="SUBMITTED")

    # users = relationship("User", secondary='user_application', back_populates='applications')

    def __repr__(self):
        return f"Application(application_id={self.application_id}, create_date={self.create_date}, application_status={self.application_status})"
    


# if __name__ == "__main__":
Base.metadata.create_all(engine)
