from server.models import engine, Applicaton
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

class ApplicationManager:
    def __init__(self):
        self.session = Session(engine)

    def get(self, user_id):
        with self.session as session:
            ans = session.execute(text(""))