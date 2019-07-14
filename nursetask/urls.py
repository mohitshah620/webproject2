from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = {
    url(r'^task/$', TaskView.as_view(), name="create"),
	url(r'^region/$', RegionView.as_view(), name="create"),
	url(r'^facility/$', FacilityView.as_view(), name="create"),
	url(r'^department/$', DepartmentView.as_view(), name="create"),
	url(r'^supervisor/$', SupervisorView.as_view(), name="create"),
	url(r'^nurse/$', NurseView.as_view(), name="create"),
	url(r'^login/$', login),
	url(r'^get_task_list/$', get_task_list),
	url(r'^add_task/$', add_task),
	url(r'^update_task/$', update_task),
	url(r'^nanalyze/$', nanalyze),
}

urlpatterns = format_suffix_patterns(urlpatterns)