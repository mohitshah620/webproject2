from rest_framework import serializers
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Task
        fields = ('tid', 'tname', 'did', 'nid', 'tdate','status')
        read_only_fields = ('tid', 'tdate')

class RegionSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Region
        fields = ('rid', 'rname')
        read_only_fields = (['rid'])

class FacilitySerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Facility
        fields = ('fid', 'fname', 'rid')
        read_only_fields = (['fid'])

class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Department
        fields = ('did', 'dname', 'fid')
        read_only_fields = (['did'])

class SupervisorSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Supervisor
        fields = ('sid', 'sname')
        read_only_fields = (['sid'])

class NurseSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Nurse
        fields = ('nid', 'nname', 'sid', 'departments','password')
        #read_only_fields = (['nid'])
