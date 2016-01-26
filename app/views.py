from flask.ext.appbuilder import AppBuilder, BaseView, expose, has_access
from flask import flash, render_template
from flask_appbuilder import SimpleFormView
from flask.ext.babelpkg import lazy_gettext as _

# class model views
from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface

from app import db, appbuilder
from forms import MyForm

from models import ContactGroup
from models import projects, resources
from models import resources_availability, resources_booking


def get_calendar_data(model_name):
    db_data = db.session.query(model_name).all()
    data = [
            (item.id,'', \
                item.start_time.strftime("%Y-%m-%dT%H:%M:%S"), \
                item.end_time.strftime("%Y-%m-%dT%H:%M:%S"), \
                '#257e4a', # color
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
                cal_data=get_calendar_data(resources_availability))

    @expose('/bookings/<int:project_id>')
    @has_access
    def bookings(self, project_id):
        # Requests for a Project resources
        return self.render_template('test.html',
                cal_header='project(%r) Resource Request/Booking Chart' % project_id,
                cal_data=get_calendar_data(resources_booking))

    @expose('/method3/<string:param1>')
    @has_access
    def method3(self, param1):
        param1 = 'Goodbye %s' % (param1)
        self.update_redirect()
        return self.render_template('base.html',param1=param1)

    @expose('/method4/')
    @has_access
    def method4(self):
        self.update_redirect()
        return self.render_template('new.html')

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


class MyFormView(SimpleFormView):
    form = MyForm
    form_title = 'This is my first form view'
    message = 'My form submitted'

    def form_get(self, form):
        form.field1.data = 'this was pre-filled data'

    def form_post(self, form):
        # post process form
        flash(self.message, 'info')

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

## FORM Submit
#appbuilder.add_view(MyFormView, "My form View", icon="fa-group", \
#        label=_('My form View'), \
#        category="My Forms", \
#        category_icon="fa-cogs")
#
#
#class GroupModelView(ModelView):
#    datamodel = SQLAInterface(ContactGroup)
#    # related_views = [ContactModelView]
#

db.create_all()

#
#appbuilder.add_view(GroupModelView, "List Groups",
#    icon = "fa-folder-open-o",
#    category = "Contacts",
#    category_icon = "fa-envelope")
#



################## Tab Menu : Project ##################
appbuilder.add_view(projects_model_view, "Projects", icon="fa-folder-open", category="Projects")
appbuilder.add_view(resources_model_view, "Resources", icon="fa-folder-open-o", category="Projects")
appbuilder.add_view(resources_availability_model_view,'resAvail', icon="fa-folder-open-o", category="Projects")
appbuilder.add_view(resources_booking_model_view,'resBooking', icon="fa-folder-open-o", category="Projects")


################## Tab Menu : Check ##################
appbuilder.add_view(project, "Summary", href='/project/summary/12', category='Check')
appbuilder.add_link("Availability", href='/project/availability/001', category='Check')
appbuilder.add_link("Bookings", href='/project/bookings/001', category='Check')
appbuilder.add_link("Method3", href='/project/method3/john', category='Check')
appbuilder.add_link("Method4", href='/project/method4', category='Check')
appbuilder.add_link("Method5", href='/project/method5', category='Check')




