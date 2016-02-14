from flask.ext.appbuilder import AppBuilder, BaseView, expose, has_access
from flask import flash, render_template
from flask_appbuilder import SimpleFormView
from flask.ext.babelpkg import lazy_gettext as _

# class model views
from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface

from app import db, appbuilder

from models import User
from models import projects, resources
from models import project_users, resources_availability, resources_booking


def get_calendar_data(model_name, color_code='#257e4a'):
    db_data = db.session.query(model_name).all()
    data = [
            (item.id,'', \
                item.start_time.strftime("%Y-%m-%dT%H:%M:%S"), \
                item.end_time.strftime("%Y-%m-%dT%H:%M:%S"), \
                color_code, # color
                ) \
            for item in db_data]
    return data

class project(BaseView):

    default_view = 'summary'

    @expose('/summary/<int:project_id>')
    @has_access
    def summary(self, project_id):
        '''
            Showcase Details of project

            * Project basic details
            * Project creation details
            * Resources attached details
            * Users tagged for resource
            * Requests details
        '''
        return self.render_template('base.html',param1='project id : %s' % project_id)

    @expose('/availability/<int:project_id>')
    @has_access
    def availability(self, project_id):
        # To know Project resources - Availability
        return self.render_template('test.html',
                cal_header='project(%r) Resource Availability Chart' % project_id,
                cal_data=get_calendar_data(resources_availability, '#257e4a') )

    @expose('/bookings/<int:project_id>')
    @has_access
    def bookings(self, project_id):
        # Requests for a Project resources
        return self.render_template('test.html',
                cal_header='project(%r) Resource Request/Booking Chart' % project_id,
                cal_data=get_calendar_data(resources_booking, 'grey'))

    @expose('/help/')
    @has_access
    def help(self):
        return self.render_template('help.html')

    @expose('/method4/<int:project_id>')
    @has_access
    def method4(self, project_id):
        '''
        shows supply and demand
        '''
        title = 'project(%r) Resource Availability Chart' % project_id
        data = get_calendar_data(resources_availability, 'green') +\
                    get_calendar_data(resources_booking, 'grey')
        return self.render_template('test.html', cal_header=title, cal_data=data)

    @expose('/method5/')
    @has_access
    def method5(self):
        self.update_redirect()
        test_data = [
                # 
                ('title','url','2016-01-12T10:30:00','2016-01-12T11:30:00', ''),
                ('title','url','2016-01-12T10:30:00','2016-01-12T12:30:00', ''),
                ('title','url','2016-01-12T11:30:00','2016-01-12T12:30:00', ''),
                ]
        return self.render_template('test.html', 
                cal_header='test page',
                cal_data=test_data)


class resources_availability_model_view(ModelView):
    datamodel = SQLAInterface(resources_availability)
    
    # label_columns = { 'resource_name' : 'resource name'}
    # list_columns = [ 'comments', 'start_time', 'end_time', 'resource_name']


class resources_booking_model_view(ModelView):
    datamodel = SQLAInterface(resources_booking)


class resources_model_view(ModelView):
    datamodel = SQLAInterface(resources)
    related_views = [
            resources_availability_model_view,
            resources_booking_model_view,
            ]


class projects_model_view(ModelView):
    datamodel = SQLAInterface(projects)
    list_columns = [ 'name', 'description']
    related_views = [
            resources_model_view,
            ]

class project_users(ModelView):
    datamodel = SQLAInterface(project_users)



db.create_all()


################## Tab Menu : Project ##################
appbuilder.add_view(projects_model_view, "Projects", icon="fa-folder-open", category="Projects")
appbuilder.add_view(resources_model_view, "Resources", icon="fa-folder-open-o", category="Projects")
appbuilder.add_view(resources_availability_model_view,'resAvail', icon="fa-folder-open-o", category="Projects")
appbuilder.add_view(resources_booking_model_view,'resBooking', icon="fa-folder-open-o", category="Projects")


################## Tab Menu : Check ##################
appbuilder.add_view(project, "Summary", href='/project/summary/12', category='Check')
appbuilder.add_link("Availability", href='/project/availability/001', category='Check')
appbuilder.add_link("Bookings", href='/project/bookings/001', category='Check')
appbuilder.add_link("Help", href='/project/help/', category='Check')
appbuilder.add_link("Method4", href='/project/method4/12', category='Check')
appbuilder.add_link("Method5", href='/project/method5', category='Check')




