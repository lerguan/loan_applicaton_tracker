from .models import engine, User, Application, UserApplication
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

class ApplicationManager:
    def __init__(self):
        self.session = Session()

# get the applications that the user currently have 
    def get(self, user_id):
        stmt = f'SELECT * FROM application a JOIN user_application ua ON a.application_id = ua.application JOIN user u ON ua.user_id = u.user_id WHERE user_id = {user_id}'
        try:
            ans = self.session.execute(text(stmt))
            if not ans:
                return "User don't have any applications!"
            results = ans.fetchall()
            self.session.commit()
            return results
        except Exception as e:
            return f'Error occurred: {str(e)}'
        finally:
            self.session.close()
        
# get the specific application
    def get_by_app_id(self, application_id):
        try:
            application = self.session.query(Application).filter_by(application_id=application_id).first()
            if not application:
                return "Application not found!"
            self.session.commit()
            return application
        except Exception as e:
            return f'Error occurred: {str(e)}'
        finally:
            self.session.close()
        

# create a new application and associate it with the user
    def post(self, create_date=None, application_status="SUBMITTED", user_id=None):
        new_application = Application(create_date=create_date, application_status=application_status)
        
        try:
            self.session.add(new_application)
            self.session.commit()

            # If user_id is provided, create the association
            if user_id:
                user = self.session.query(User).filter_by(user_id=user_id).first()
                if user:
                    new_application.users.append(user)  # Associate the application with the user
                    self.session.commit()  # Commit changes for the user association
                else:
                    self.session.rollback()
                    return 'User not found!'

            return f'Application created successfully with ID {new_application.application_id}'
        except IntegrityError:
            self.session.rollback()
            return 'Error: Could not create application.'
        except Exception as e:
            self.session.rollback()
            return f'Error occurred: {str(e)}'
        

# Retrieve the status of a specific application by application_id
    def get_status(self, application_id):

        application = self.session.query(Application).filter_by(application_id=application_id).first()
        
        if not application:
            return 'Application not found!'
        
        return application.application_status
    
# Update the status of a specific application by application_id.
    def patch_status(self, application_id, new_status):

        application = self.session.query(Application).filter_by(application_id=application_id).first()
        
        if not application:
            return 'Application not found!'

        try:
            application.application_status = new_status  # Update the status
            self.session.commit()  # Commit the changes
            return f'Application status updated to {new_status}'
        except Exception as e:
            self.session.rollback()
            return f'Error occurred: {str(e)}'

    def delete(self, application_id):
        """
        Delete a specific application by application_id.
        """
        application = self.session.query(Application).filter_by(application_id=application_id).first()

        if not application:
            return 'Application not found!'

        try:
            self.session.delete(application)  # Delete the application
            self.session.commit()  # Commit the deletion
            return 'Application deleted successfully.'
        except Exception as e:
            self.session.rollback()
            return f'Error occurred: {str(e)}'

    # def get_unssigned_application(self):
    #     pass