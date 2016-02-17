'''

Sample records creation for following tables

* user
* resources
* avail
* booking

'''
import datetime

from app import appbuilder, db
from flask_appbuilder.security.sqla.models import User, Role
from app.models import projects_model, project_users_model
from app.models import resources_model, resources_booking_model, resources_availability_model

session = db.session()


#
# generic function
#

def csv_to_list(data):
  data = data.strip().splitlines()
  data = [ x.split(',') for x in data ]
  return data

def clean_up_model(model_name):
  session = db.session()
  for x in session.query(model_name).all():
    session.delete(x)
  session.commit()

#
# User accounts creation
#
test_users = '''
bot1,fn1,ln1,bot1231@gmail.com
bot2,fn2,ln2,bot2122@gmail.com
bot3,fn3,ln3,bot312313@gmail.com
'''

def create_test_user():
  test_users = csv_to_list(test_users)
  for u, f, l, e in test_users:
    session.add(User(username=u, first_name=f, last_name=l, email=e, password=u))
  session.commit()

#
# Project 
#

test_projects = '''
test_project_01,this_is_test_prject01
test_project_02,this_is_test_prject02
test_project_03,this_is_test_prject03
'''


def create_test_projects():
  data = csv_to_list(test_projects)
  for name, description in data:
    p = projects_model(name=name, description=description)
    session.add(p)
  session.commit()


#
# Resources
#

test_resources = '''
res_01,this_is_a_test_resource
res_02,this_is_a_test_resource
res_03,this_is_a_test_resource
'''


def create_test_resources():
  data = csv_to_list(test_resources)
  avail_projects = session.query(projects_model).all()
  for p in avail_projects:
    for name, description in data:
      name = p.name + ' ' + name
      description = p.name + ' ' + description
      session.add( resources_model(name=name, project_id=p.id, description=description))
  session.commit()


#
# resources
#


def create_test_resources_avail():
  #
  for month in range(1, 3):
    for date in range(1, 5):
      for time in range(9, 11):
        start = datetime.datetime(2016, 1, date, time )
        end  = datetime.datetime(2016, 1, date, time + 5 )
        for res in session.query(resources_model).all():
          res_avail =  resources_availability_model(resource_id=res.id, start_time=start, end_time=end, comments='test resource' + str(res.id) )
          session.add(res_avail)
  session.commit()


def create_test_resources_book():
  #
  for month in range(1,3):
    for date in range(3, 6):
      for time in range(8, 10):
        start = datetime.datetime(2016, 1, date, time )
        end  = datetime.datetime(2016, 1, date, time + 5 )
        for res in session.query(resources_model).all():
          res_avail =  resources_booking_model(resource_id=res.id, start_time=start, end_time=end, comments='test resource' + str(res.id) )
          session.add(res_avail)
  session.commit()


if __name__ == '__main__':
  clean_up_model(resources_model)
  clean_up_model(projects_model)

  clean_up_model(resources_booking_model)
  clean_up_model(resources_availability_model)

  create_test_projects()
  create_test_resources()

  create_test_resources_book()
  create_test_resources_avail()

