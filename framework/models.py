from typing import Set
from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone
from django.contrib import admin
import uuid

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

class Mission(models.Model):
    STATE = {
        ('NA', 'Not Attributed'),
        ('IQ', 'In Queue'),
        ('IP', 'In Process'),
        ('PA', 'Paused'),
        ('CF', 'Conflict'),
        ('FA', 'Failed'),
        ('CO', 'Completed'),
        ('AR', 'Archived'),
    }

    ACTIONS = {
        ('IQ', 'Commencer'),
        ('IP', 'Terminer'),
        ('PA', 'Reprendre'),
        ('CO', 'Complétée'),
    }

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    technician = models.ForeignKey(Technician, on_delete=SET_NULL, blank=True, null=True)
    terminal = models.ForeignKey(Terminal, on_delete=SET_NULL, blank=True, null=True)

    date = models.DateTimeField('Date de la mission')
    state = models.CharField(max_length=2, choices=STATE, default='NA')
    false_positives = models.IntegerField(default=0)

    @property
    def date_formated(self):
        return self.date.strftime("%d %b. %H:%M")

    @property
    def formated_state(self):
        for state in self.STATE:
            if state[0] == self.state:
                return state[1]
        return self.state

    @property
    def formated_action(self):
        for action in self.ACTIONS:
            if action[0] == self.state:
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