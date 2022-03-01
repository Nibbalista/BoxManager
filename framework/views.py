from re import template
from typing import TYPE_CHECKING
from django import http, forms
from django.db.models.fields import IPAddressField
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core import serializers

import json

import datetime

from .models import *

# Create your views here.
class IndexView(TemplateView):
    template_name = 'framework/index.html'

class LoginView(TemplateView):
    template_name = 'framework/login.html'

class MissionsView(TemplateView):
    template_name = 'framework/missions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['missions_week'] = Mission.objects.filter(date__startswith=datetime.date.today())
        context['missions_future'] = Mission.objects.filter(date__gt=datetime.date.today() + datetime.timedelta(days=1)).order_by('date')
        context['missions_count'] = context['missions_week'].count
        context['future_count'] = context['missions_future'].count

        return context

class MissionOverView(TemplateView):
    template_name = 'framework/mission-overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mission = Mission.objects.get(uuid=kwargs['mission_uuid'])   
        avancement = 100
        if avancement==0:
            mission.commencer()
        elif avancement==5:
            mission.continuer()
        elif avancement==100:
            mission.terminer()
        #elif avancement==101:
        #    mission.finish()
        mission.save()
        finish = False
        if mission.status == 'CO':
            finish= True
            
        context['mission'] = mission
        return context

class TerminalOverview(TemplateView):
    #mission start check

    template_name = 'framework/newTerminal.html'

    #pass the actions objects
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mission = Mission.objects.get(uuid=kwargs['mission_uuid'])
        terminal = Terminal.objects.get(uuid=mission.terminal.uuid)
        context['mission'] = mission
        context['terminal'] = terminal

        actions = Action.objects.filter(mission=mission)

        context['actions'] = actions

        pendingActions = actions.filter(Q(action="DE") | Q(action="WI"))
        print(pendingActions)
        context['actionsLength'] = pendingActions.count

        return context

class LockerDetails(TemplateView):
    template_name = 'framework/LockerDetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mission = Mission.objects.get(uuid=kwargs['mission_uuid'])
        actions = Action.objects.filter(mission=mission)
        for action in actions:
            if action.locker.uuid == kwargs['locker_uuid']:
                actions = action
                break
        
        context['action'] = actions
        return context

class ErrorPage(TemplateView):
    template_name = 'framework/error.html'


class QRDisplay(TemplateView):
    template_name = 'framework/qrcode.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['locker_uuid'] = kwargs['locker_uuid']
        return context
        
