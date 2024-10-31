from .models import engine, User, Application, UserApplication
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

class ApplicationNotFoundException(Exception):
    def __init__(self, id):
        super().__init__(f'Application with ID {id} not found.')

class ApplicationManager:
    def __init__(self):
        self.session = Session()

# get the applications that the user currently have 
    def get(self, user_id):
        stmt = text('SELECT * FROM application WHERE application_id in (SELECT application_id FROM user_application WHERE user_id = :user_id)')
        try:
            ans = self.session.execute(stmt, {'user_id': user_id})
            results = ans.fetchall()
            self.session.commit()
            if not results:
                raise ApplicationNotFoundException(user_id)
            return results
        except Exception as e:
            return f'Error occurred: {str(e)}'
        finally:
            self.session.close()
        
# get the specific application
    def get_by_app_id(self, application_id):
        stmt = text('SELECT * FROM application WHERE application_id = :application_id')
        try:
            ans = self.session.execute(stmt, {'application_id': application_id})
            result = ans.fetchall()
            self.session.commit()
            if not result:
                raise ApplicationNotFoundException(application_id)
            return result
        except Exception as e:
            return f'Error occurred: {str(e)}'
        finally:
            self.session.close()
        

# create a new application and associate it with the user
    def post(self, user_id, application_id):
        new_application_assignment = UserApplication(user_id=user_id, application_id=application_id)
        try:
            self.session.add(new_application_assignment)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            return 'Error: Could not create application.'
        except Exception as e:
            self.session.rollback()
            return f'Error occurred: {str(e)}'
        

# Retrieve the status of a specific application by application_id
    def get_status(self, user_id, application_id):
        stmt = text('SELECT a.application_id, application_status FROM application a JOIN user_application ua ON a.application_id = ua.application_id WHERE a.application_id = :application_id AND user_id = :user_id')
        try:    
            ans = self.session.execute(stmt, {'application_id': application_id, 'user_id': user_id})
            result = ans.fetchall()
            self.session.commit()
            if not result:
                raise ApplicationNotFoundException(application_id)
            return result
        except Exception as e:
            return f'Error occurred: {str(e)}'
        finally:
            self.session.close()
    
# Update the status of a specific application by application_id.
    def patch_status(self, application_id, new_status):
        stmt = text('UPDATE application SET application_status = :new_status WHERE application_id = :application_id')
        try:
            self.session.execute(stmt, {'new_status': new_status, 'application_id': application_id})
            self.session.commit()
            return f'Application status updated to {new_status}'
        except Exception as e:
            self.session.rollback()
            return f'Error occurred: {str(e)}'
        finally:
            self.session.close()

    # def delete(self, application_id):
    #     """
    #     Delete a specific application by application_id.
    #     """
    #     application = self.session.query(Application).filter_by(application_id=application_id).first()

    #     if not application:
    #         return 'Application not found!'

    #     try:
    #         self.session.delete(application)  # Delete the application
    #         self.session.commit()  # Commit the deletion
    #         return 'Application deleted successfully.'
    #     except Exception as e:
    #         self.session.rollback()
    #         return f'Error occurred: {str(e)}'