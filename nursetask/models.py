from django.db import models


# Create your models here.
class Region(models.Model):
    rid = models.IntegerField(primary_key=True, auto_created=True)
    rname = models.CharField(max_length=10)

    def _str_(self):
        """Return a human readable representation of the model instance."""
        return "{}, {}".format(self.rid,self.name)

class Facility(models.Model):
    fid = models.IntegerField(primary_key=True,  auto_created=True)
    rid = models.ForeignKey(Region, on_delete=models.CASCADE)
    fname = models.CharField(max_length=10)

    def _str_(self):
        """Return a human readable representation of the model instance."""
        return "{}, {}, {}".format(self.fid, self.rid, self.fname)
    
class Department(models.Model):
    did = models.IntegerField(primary_key=True, auto_created=True)
    fid = models.ForeignKey(Facility, on_delete=models.CASCADE)
    dname = models.CharField(max_length=10)

    def _str_(self):
        """Return a human readable representation of the model instance."""
        return "{}, {}, {}".format(self.did, self.fid, dname)

class Supervisor(models.Model):
    sid = models.IntegerField(primary_key=True, auto_created=True)
    sname = models.CharField(max_length=10)

    def _str_(self):
        """Return a human readable representation of the model instance."""
        return "{}, {}".format(self.sid, self.sname)

class Nurse(models.Model):
    nid = models.IntegerField(primary_key=True)
    nname = models.CharField(max_length=10)
    sid = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    departments = models.ManyToManyField(Department, related_name= 'departments')
    password = models.CharField(max_length=10, default='pass')

    def _str_(self):
        """Return a human readable representation of the model instance."""
        return "{}, {}, {}, {}".format(self.nid, self.nname, self.sid, self.departments)
    

class Task(models.Model):
    tid = models.IntegerField(primary_key=True, auto_created=True)
    tname = models.CharField(max_length=10)
    did = models.ForeignKey(Department, on_delete=models.CASCADE)
    nid = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    tdate = models.DateField(blank=False, auto_now=True)
    status = models.BooleanField(default= False)

    @classmethod
    def create(cls, tname,nurse,department):
        task = cls(tname=tname, nid=nurse, did=department)
        # do something with the book
        return task
    def _str_(self):
        """Return a human readable representation of the model instance."""
        return "{}, {}, {}, {}, {}".format(self.tid, self.tname, self.did, self.nid, self.tdate)