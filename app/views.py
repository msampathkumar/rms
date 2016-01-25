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

class MyView(BaseView):

    default_view = 'method1'

    @expose('/method1/')
    @has_access
    def method1(self):
        # do something with param1
        # and return to previous page or index
        return 'Hello'

    @expose('/method2/<string:param1>')
    @has_access
    def method2(self, param1):
        # do something with param1
        # and render template with param
        param1 = 'Goodbye %s' % (param1)
        return param1

    @expose('/method3/<string:param1>')
    @has_access
    def method3(self, param1):
        # do something with param1
        # and render template with param
        param1 = 'Goodbye %s' % (param1)
        self.update_redirect()
        return self.render_template('method3.html',param1=param1)


    @expose('/method4/')
    @has_access
    def method4(self):
        self.update_redirect()
        return self.render_template('new.html')

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


appbuilder.add_view(MyView, "Method1", category='My View')
appbuilder.add_link("Method2", href='/myview/method2/john', category='My View')
appbuilder.add_link("Method3", href='/myview/method3/john', category='My View')
appbuilder.add_link("Method4", href='/myview/method4', category='My View')
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
appbuilder.add_view(projects_model_view, "Projects", 
    icon="fa-folder-open",
    category="Projects")

appbuilder.add_view(resources_model_view, "Resources",
    icon="fa-folder-open-o",
    category="Projects")

appbuilder.add_view(resources_availability_model_view,'resAvail',
    icon="fa-folder-open-o",
    category="Projects")

appbuilder.add_view(resources_booking_model_view,'resBooking',
    icon="fa-folder-open-o",
    category="Projects")
