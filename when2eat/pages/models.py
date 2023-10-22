from django.db import models

class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.start_time)

class Status(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    time_slot = models.ForeignKey('TimeSlot', on_delete=models.CASCADE)
    status = models.CharField(max_length=5, choices=(('b', 'busy'), ('f', 'free'), ('e', 'eaten'), ('p', 'plan')))

    def __str__(self):
        return str(self.person) + ' - ' + str(self.time_slot)

class Plan(models.Model):
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return 'plan ' + ' @ ' + self.location + ' (' + str(self.start_time) + ' - ' + str(self.end_time) + ')'
 
class Person(models.Model):
    name = models.CharField(max_length=32)
    time_slots = models.ManyToManyField('TimeSlot', through='Status', blank=True)
    plans = models.ManyToManyField('Plan', blank=True)
    preference = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
