from flask.ext.appbuilder import Model
from flask.ext.appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

from flask_appbuilder.security.sqla.models import User

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""

class projects_model(Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    description =  Column(String(500), nullable=False)

    def __repr__(self):
        return 'Project:%s' % self.name


class resources_model(Model):
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects_model.id'))
    name =  Column(String(150), unique = True, nullable=False)
    description =  Column(String(500), nullable=True)
    
    # relationship
    project_name = relationship("projects_model")

    def __repr__(self):
        return '%s:%s' % (self.project_name, self.name)

class resources_availability_model(Model):
    id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey('resources_model.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    comments = Column(String(500), nullable=True)

    # relationship
    resource_name = relationship('resources_model')

    def __repr__(self):
        return 'ResourceAvailability:%s' % self.id

class resources_booking_model(Model):
    id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey('resources_model.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    comments = Column(String(500), nullable=True)

    # relationship
    resource_name = relationship('resources_model')

    def __repr__(self):
        return 'resources_model Booking id:%r>' % self.id


class project_users_model(Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    user_name = relationship("User")
    project_id = Column(Integer, ForeignKey('projects_model.id'), nullable=False)
    project_name = relationship("projects_model")
