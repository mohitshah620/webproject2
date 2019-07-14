from models import *

def nurse_details(username, password):
  nurse_details = {}
  nurse = Nurse.objects.get(nname = username, password = password)
  if nurse:
    departments = []
	for department in nurse.departments.iterator():
	  departments.append(department.dname)
	nurse_details['msg'] = 'User exists'
	nurse_details['name'] = nurse.nname
	nurse_details['id'] = nurse.nid
	nurse_details['supervisor'] = Supervisor.objects.get(nurse.sid).sname
	nurse_details['departments'] = departments
	print("Nurse details")
  else:
    nurse_details['msg'] = 'User doesn't exists'
    print("No such user")
	
	

