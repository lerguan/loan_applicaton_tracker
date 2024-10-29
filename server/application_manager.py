from server.models import Session, Applicaton
from sqlalchemy.exc import IntegrityError

class ApplicationManager:
    def __init__(self):
        self.session = Session()

    def get(self, user_id):
        application = self.session.query(Applicaton).filter()