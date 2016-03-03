from flask.ext.appbuilder import AppBuilder, BaseView, expose, has_access
from flask import flash, render_template, jsonify
from flask_appbuilder import SimpleFormView
from flask.ext.babelpkg import lazy_gettext as _

# class model views
from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface

from app import db, appbuilder

from models import projects_model, resources_model, User
from models import project_users_model, resources_availability_model, resources_booking_model

from sqlalchemy import func

import datetime

#
#  Custome views/reports
#

def get_model_data(db_model):
    # fetches all the data in table
    return db.session.query(db_model).all()


def get_model_item(db_model, id=1):
    # fetches one item as per index id
    q = db.session.query(db_model).filter(db_model.id==id).all()
    if q:
        return q[0] # id always unique  - only item will be there
    else:
        return 


def get_project_item(project_id):
    return get_model_item(projects_model, project_id)


def get_project_users(project_id):
    data = db.session.query(project_users_model)\
        .join(User, project_users_model.user_id==User.id)\
        .add_columns(User.first_name, User.last_name)\
        .filter(project_users_model.project_id==project_id)\
        .all()
    new = []
    for item, first_name, last_name in data:
        item.first_name = first_name
        item.last_name = last_name
        new.append(new)
    # data = db.session.query(project_users_model).filter(project_users_model.project_id==project_id).all()
    # return data
    return new


def get_project_details(project_id):
    '''
    Returns :
        * project 
        * project - users
    '''
    project = get_model_item(projects_model, project_id)
    project_users = get_project_users(project_id)
    return [
            project, # project object
            project_users, # project user
            ]


def get_calendar_data(db_model, color_code='#257e4a'):
    db_data = get_model_data(db_model)
    data = [
            (item.id,'', \
                item.start_time.strftime("%Y-%m-%dT%H:%M:%S"), \
                item.end_time.strftime("%Y-%m-%dT%H:%M:%S"), \
                color_code, # color
                ) \
            for item in db_data]
    return data




def get_model_group_count(db_model):
    # 
    my_group_by_col = func.Date(db_model.start_time)
    start_date_01 = datetime.datetime(2016, 1, 1, 0, 0)
    start_date_02 = datetime.datetime(2016, 1, 29, 0, 0)
    sam = db.session.query(my_group_by_col, func.count(my_group_by_col)) \
        .filter(my_group_by_col >= start_date_01) \
        .filter(my_group_by_col < start_date_02) \
        .group_by(my_group_by_col)
    
    return sam.all()


def get_model_group_count_dict(db_model=resources_availability_model):
    return { x:y for x,y in get_model_group_count(db_model)}


def get_monthly_supply_demand():
    #
    supply = get_model_group_count_dict(resources_availability_model)
    demand = get_model_group_count_dict(resources_booking_model)
    all_dates = set(supply.keys() + demand.keys())
    return [ (x, supply.get(x,0), demand.get(x,0)) for x in all_dates]


class project(BaseView):

    default_view = 'all_projects'

    @expose('/')
    @expose('/all')
    # @has_access
    def all_projects(self):
        '''
        Links to all projects
        '''
        data = get_model_data(projects_model)
        return self.render_template('projects.html',param1=data)

    @expose('/<int:project_id>/summary')
    # @has_access
    def summary(self, project_id):
        '''
            Showcase Details of project

            * Project basic details
            * Project creation details
            * Resources attached details
            * Users tagged for resource
            * Requests details
        '''

        project, project_users = get_project_details(project_id)
        if not project:
            abort(404)
        return self.render_template('project_details.html',
            project=project, # get selected project
            users_list=project_users,
            resources_list=[])
    
    @expose('/<int:project_id>/availability')
    # @has_access
    def availability(self, project_id):
        # To know Project resources - Availability
        return self.render_template('calendar.html',
                project =  get_project_item(project_id),
                cal_header='Availability Chart',
                cal_data=get_calendar_data(resources_availability_model, '#257e4a') )

    @expose('/<int:project_id>/bookings')
    # @has_access
    def bookings(self, project_id):
        # Requests for a Project resources
        return self.render_template('calendar.html',
                project =  get_project_item(project_id),
                cal_header='Booking Requests',
                cal_data=get_calendar_data(resources_booking_model, 'grey'))

    @expose('/help/')
    # @has_access
    def help(self):
        return self.render_template('help.html')

    @expose('/test/')
    # @has_access
    def test(self):
        import json
        graph_data = get_monthly_supply_demand()
        return self.render_template('graph.html',
                graph_header='Availability (Supply & Demand) Requests',
                #graph_data=get_calendar_data(resources_availability_model, '#257e4a')
                graph_data=graph_data
                )

    @expose('/method4/<int:project_id>')
    # @has_access
    def method4(self, project_id):
        '''
        shows supply and demand
        '''
        title = 'project(%r) Resource Availability Chart' % project_id
        data = get_calendar_data(resources_availability_model, 'green') +\
                    get_calendar_data(resources_booking_model, 'grey')
        return self.render_template('calendar.html', cal_header=title, cal_data=data)

    @expose('/method5/')
    # @has_access
    def method5(self):
        self.update_redirect()
        test_data = [
                # 
                ('title','url','2016-01-12T10:30:00','2016-01-12T11:30:00', ''),
                ('title','url','2016-01-12T10:30:00','2016-01-12T12:30:00', ''),
                ('title','url','2016-01-12T11:30:00','2016-01-12T12:30:00', ''),
                ]
        return self.render_template('calendar.html', 
                cal_header='Test - Calendar page',
                cal_data=test_data)


#
#  Table/Model views
#

class resources_availability(ModelView):
    datamodel = SQLAInterface(resources_availability_model)


class resources_booking(ModelView):
    datamodel = SQLAInterface(resources_booking_model)


class resources(ModelView):
    datamodel = SQLAInterface(resources_model)
    related_views = [
            resources_availability,
            resources_booking,
            ]


class projects(ModelView):
    datamodel = SQLAInterface(projects_model)
    list_columns = [ 'name', 'description']
    related_views = [
            resources,
            ]


class project_users(ModelView):
    datamodel = SQLAInterface(project_users_model)


db.create_all()


################## Tab Menu : Project ##################
appbuilder.add_view(projects, "Projects", icon="fa-folder-open", category="Resource_Providers")
appbuilder.add_view(resources, "Resources", icon="fa-folder-open-o", category="Resource_Providers")
appbuilder.add_view(project_users, "project_users", icon="fa-folder-open", category="Resource_Providers")
appbuilder.add_view(resources_availability,'resAvail', icon="fa-folder-open-o", category="Resource_Providers")
appbuilder.add_view(resources_booking,'resBooking', icon="fa-folder-open-o", category="Resource_Providers")


################## Tab Menu : Check ##################
appbuilder.add_view(project, "Projects", href='/project/all', category='stakeholders')
# appbuilder.add_view(project, "Summary", href='/project/summary/12', category='stakeholders') # internal
# appbuilder.add_link("Availability", href='/project/availability/001', category='stakeholders') # internal
# appbuilder.add_link("Bookings", href='/project/bookings/001', category='stakeholders') # internal
appbuilder.add_link("Help", href='/project/help/', category='Help')
appbuilder.add_link("Test", href='/project/test/', category='Test')
appbuilder.add_link("Method4", href='/project/method4/12', category='stakeholders')
appbuilder.add_link("Method5", href='/project/method5', category='stakeholders')




