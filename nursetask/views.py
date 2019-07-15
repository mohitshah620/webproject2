from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import *
from .models import *
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
import copy

@require_http_methods(["POST"])
@csrf_exempt
def login(request):
    # I can assume now that only GET or POST requests make it this far
    # ...
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    nurse_details = {}
    try:
        nurse = Nurse.objects.get(nid = username, password = password)
    except Nurse.DoesNotExist:
        nurse_details['msg'] = username + " User doesn't exists"
        return HttpResponse(json.dumps(nurse_details), content_type="application/json")
    if nurse is not None:
        departments = []
        for department in nurse.departments.iterator():
            departments.append(department.dname)
        nurse_details['msg'] = 'User exists'
        nurse_details['name'] = nurse.nname
        nurse_details['id'] = nurse.nid
        nurse_details['supervisor'] = nurse.sid.sname
        nurse_details['departments'] = departments
        print("Nurse details")
    return HttpResponse(json.dumps(nurse_details), content_type="application/json")

@require_http_methods(["GET"])
def get_task_list(request):
    nurse_id = request.GET['username']
    department_name = request.GET['department']
    tasks = {}
    try:
        nurse = Nurse.objects.get(nid=nurse_id)
    except Nurse.DoesNotExist:
        tasks['msg'] = nurse_id + " Nurse doesn't exists in the database"
        return HttpResponse(json.dumps(tasks), content_type="application/json")

    try:
        department = Department.objects.get(dname=department_name)
    except Department.DoesNotExist:
        tasks['msg'] = department_name + " department doesn't exists in the database"
        return HttpResponse(json.dumps(tasks), content_type="application/json")

    Tasks = Task.objects.filter(did=department.did,nid=nurse.nid,tdate=datetime.date.today())
    task = {}
    task_list = []
    for temp in Tasks:
        task['id'] = temp.tid
        task['name'] = temp.tname
        task['status'] = 'complete' if temp.status else 'incomplete'
        task['date'] = temp.tdate.strftime('%m/%d/%Y')
        task_list.append(task)
    tasks['tasks'] = task_list
    return HttpResponse(json.dumps(tasks), content_type="application/json")

@require_http_methods(["POST"])
@csrf_exempt
def add_task(request):
    nurse_id = request.POST.get('nurse_id', '')
    department_name = request.POST.get('department_name', '')
    task_name = request.POST.get('task', '')
    task = {}
    try:
        nurse = Nurse.objects.get(nid=nurse_id)
    except Nurse.DoesNotExist:
        task['msg'] = nurse_id + " Nurse doesn't exists in the database"
        return HttpResponse(json.dumps(task), content_type="application/json")

    try:
        department = Department.objects.get(dname=department_name)
    except Department.DoesNotExist:
        task['msg'] = department_name + " department doesn't exists in the database"
        return HttpResponse(json.dumps(task), content_type="application/json")

    temp = Task.objects.create(tname=task_name, nid=nurse, did=department)
    
    task['task_name'] = temp.tname
    task['status'] = temp.status
    task['id'] = temp.tid

    return HttpResponse(json.dumps(task), content_type="application/json")


@require_http_methods(["POST"])
@csrf_exempt
def update_task(request):
    nurse_id = request.POST.get('nurse_id', '')
    task_id = int(request.POST.get('task_id', ''))
    department_name = request.POST.get('department_name', '')
    tasks = {}
    try:
        nurse = Nurse.objects.get(nid=nurse_id)
    except Nurse.DoesNotExist:
        tasks['msg'] = nurse_id+" Nurse doesn't exists in the database"
        return HttpResponse(json.dumps(tasks), content_type="application/json")

    try:
        department = Department.objects.get(dname=department_name)
    except Department.DoesNotExist:
        tasks['msg'] = department_name+" department doesn't exists in the database"
        return HttpResponse(json.dumps(tasks), content_type="application/json")

    temp = Task.objects.filter(did=department,nid=nurse,tid=task_id)
    if len(temp) == 0:
        tasks['msg'] = str(task_id)+" task doesn't exists in the database"
        return HttpResponse(json.dumps(tasks), content_type="application/json")
    temp.update(status=True)
    tasks['msg'] = str(temp[0].nid) +" task status updated"
    return HttpResponse(json.dumps(tasks), content_type="application/json")

@require_http_methods(["POST"])
@csrf_exempt
def nanalyze(request):
	mssg = {}
	analytics = {}
	average_tasks_per_department = {}
	average_tasks_per_nurse_under_supervisor = {}
	departments = Department.objects.all()
	for department in departments:
		task_count_per_department = Task.objects.filter(did = department).count()
		nurse_count_per_department = Nurse.objects.filter(departments = department).count()
		if nurse_count_per_department != 0:
			average_tasks_per_department[department.dname] = task_count_per_department / nurse_count_per_department
		else:
			average_tasks_per_department[department.dname] = 0


	for supervisor in Supervisor.objects.all():
		nurses_under_supervisor = Nurse.objects.filter(sid = supervisor)
		task_per_supervisor = 0
		for nurse in nurses_under_supervisor:
			task_per_supervisor = task_per_supervisor + Task.objects.filter(nid = nurse).count()
		nurse_count_under_supevisor = nurses_under_supervisor.count()
		if nurse_count_under_supevisor != 0:
			average_tasks_per_nurse_under_supervisor[supervisor.sname] = task_per_supervisor / nurse_count_under_supevisor
		else:
			average_tasks_per_nurse_under_supervisor[supervisor.sname] = 0
	analytics['average_tasks_per_department'] = average_tasks_per_department
	analytics['average_tasks_per_nurse_under_supervisor'] = average_tasks_per_nurse_under_supervisor

	
	temp = []
	for region in Region.objects.all():
		number_of_tasks_per_department_per_facility_per_region = {}
		number_of_tasks_per_department_per_facility_per_region['region'] = region.rname
		facility_under_region = Facility.objects.filter(rid=region)
		for facility in facility_under_region:
			temp_2 = copy.deepcopy(number_of_tasks_per_department_per_facility_per_region)
			temp_2['facility'] = facility.fname
			department_under_facility = Department.objects.filter(fid=facility)
			for department in department_under_facility:
				temp_3 = copy.deepcopy(temp_2)
				temp_3['department'] = department.dname
				temp_3['number_of_tasks'] = Task.objects.filter(did=department).count()
				temp.append(temp_3)
	analytics['number_of_tasks_per_department_per_facility_per_region'] = temp
	return HttpResponse(json.dumps(analytics), content_type="application/json")




	

class TaskView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()

class RegionView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()
        
class FacilityView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()
        
class DepartmentView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()
        
class SupervisorView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Supervisor.objects.all()
    serializer_class = SupervisorSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()
        
class NurseView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()