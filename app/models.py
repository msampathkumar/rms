from flask.ext.appbuilder import Model
from flask.ext.appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name


class projects(Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    description =  Column(String(500), unique = True, nullable=False)

    def __repr__(self):
        return 'Project:%r' % self.name

class resources(Model):
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    name =  Column(String(150), unique = True, nullable=False)
    description =  Column(String(500), nullable=True)
    
    # relation ship
    project_name = relationship("projects")

    def __repr__(self):
        return '%s:%r' % (self.project_name, self.name)

class resources_availability(Model):
    id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey('resources.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    comments = Column(String(500), nullable=True)

    # relationship
    resource_name = relationship('resources')

    def __repr__(self):
        return '<resources_availability id:%r>' % self.id

class resources_booking(Model):
    id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey('resources.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    comments = Column(String(500), nullable=True)

    # relationship
    resource_name = relationship('resources')

    def __repr__(self):
        return '<resources_booking id:%r>' % self.id


