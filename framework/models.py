from typing import Set
from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone
from django.contrib import admin
import uuid
from django_fsm import FSMField, transition

# Create your models here.
class Terminal(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    display_name = models.CharField(max_length=64)
    adress = models.CharField(max_length=200)
    code = models.CharField(max_length=64)

    STATE = {
        ('ON', 'In Service'),
        ('OFF', 'Offline'),
        ('ERR', 'Error'),
    }
    state = models.CharField(max_length=3, choices=STATE, default='ON')

    def __str__(self):
         return "%s" % (self.display_name)

class Locker(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE, blank=True, null=True)
    number = models.IntegerField(default=0)

    STATE = {
        ('ON', 'In Service'),
        ('OFF', 'Offline'),
        ('ERR', 'Error'),
    }
    state = models.CharField(max_length=3, choices=STATE, default='ON')

    def __str__(self):
            return "%s #%s" % (self.terminal.display_name, self.number)

class Technician(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=SET_NULL, blank=True, null=True)
    code = models.CharField(max_length=32)
    false_positives = models.IntegerField(default=0)

    def __str__(self):
         return "%s %s" % (self.user.first_name, self.user.last_name)

class Product(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    terminal = models.ForeignKey(Terminal, on_delete=SET_NULL, blank=True, null=True)
    locker = models.ForeignKey(Locker, on_delete=SET_NULL, blank=True, null=True)
    
    reference = models.CharField(max_length=50, default='Smartphone')
    physical_state = models.CharField(max_length=64)
    software_diagnostic = models.CharField(max_length=64)
    comment = models.CharField(max_length=256, null=True)

    def __str__(self):
        return "%s" % (self.reference)    

MISSIONSTATUS = ('NA','IQ','IP', 'PA', 'CF', 'FA', 'CO')
LITTERALMISSIONSTATUS = ('Not Attributed', 'In Queue', 'In Process', 'Paused', 'Conflict', 'Failed', 'Finish') 
MISSIONSTATUS=list(zip(MISSIONSTATUS, LITTERALMISSIONSTATUS ))

class Mission(models.Model):
    class STATUS:
        NA = 'Not Attributed'
        IP = 'In Queue'
        PA = 'Paused'
        CO = 'Completed'
        
    #STATE ={(STATUS.NA ,'Init'),(STATUS.IP ,'In Process')(STATUS.PA, 'Stopped'), (STATUS.CO, 'Complétée')}

    ACTIONS = {
        ('IQ', 'Commencer'),
        ('IP', 'Complétée'),
        ('PA', 'Reprendre'),
        ('CO', 'Terminer'),
    }

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    technician = models.ForeignKey(Technician, on_delete=SET_NULL, blank=True, null=True)
    terminal = models.ForeignKey(Terminal, on_delete=SET_NULL, blank=True, null=True)

    date = models.DateTimeField('Date de la mission')
    status = FSMField(verbose_name='status_mission', 
                      choices=MISSIONSTATUS, 
                      default = MISSIONSTATUS[0])
    false_positives = models.IntegerField(default=0)

    @transition(field=status, source='NA', target='IQ')
    def commencer(self):
        print()
        pass
    
    @transition(field=status, source='IQ', target='IP')
    def continuer(self):
        print()
        pass
    
    @transition(field=status, source='IP', target='CO')
    def terminer(self):
        print()
        pass
    
    finish = False
    if status == 'CO':
        finish= True
        
        
    @transition(field=status, source='CO', target='FI')
    def finish(self):
        finish = True
        print()
        pass
    
    # def getpaused():
    #     return False
    # @transition(field=status, source='*', target='PA', condition=[getpaused])
    # def commencer(self):
    #     print()
    #     pass

    @property
    def date_formated(self):
        return self.date.strftime("%d %b. %H:%M")

    @property
    def formated_state(self):
        for state in MISSIONSTATUS:
            if state[0] == self.status:
                return state[1]
        return self.status

    @property
    def formated_action(self):
        for action in self.ACTIONS:
            if action[0] == self.status:
                return action[1]
        return 'na'

    def __str__(self):
         return "%s - %s" % (self.terminal.display_name, self.date)

class Action(models.Model):
    ACTIONS = {
        ('NA', 'Not Assessed'),
        ('VA', 'Validated'),
        ('DE', 'Deposit'),
        ('WI', 'Withdrawal'),
    }
    STATE = {
        ('WA', 'Waiting'),
        ('IT', 'In Transit'),
        ('DO', 'Done'),
        ('ER', 'Error'),
    }

    mission = models.ForeignKey(Mission, on_delete=SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=SET_NULL, blank=True, null=True)
    
    action = models.CharField(max_length=2, choices=ACTIONS, default='NA')
    state = models.CharField(max_length=2, choices=STATE, default='WA')

    @property
    def locker(self):
        return self.product.locker

    @property
    def formated_action(self):
        for state in self.ACTIONS:
            if state[0] == self.action:
                return state[1]
        return self.action

    def __str__(self):
         return "%s - #%s %s" % (self.mission.terminal.display_name, self.product.locker.number, self.action)