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
        context['mission'] = mission
        return context

class TerminalOverview(TemplateView):
    #mission start check

    template_name = 'framework/terminal.html'

    #pass the actions objects
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mission = Mission.objects.get(uuid=kwargs['mission_uuid'])
        terminal = Terminal.objects.get(uuid=mission.terminal.uuid)
        context['mission'] = mission
        context['terminal'] = terminal

        actions = Action.objects.filter(mission=mission)
        actions_ordered = {}
        for action in actions:
            actions_ordered[action.locker.number] = action
        context['actions'] = actions_ordered
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
        

        print(actions)
        context['action'] = actions
        return context

class ErrorPage(TemplateView):
    template_name = 'framework/error.html'


# class QRScanner('TemplateView'):
#     template_name = 'framework/qrcode.html'

#     def get_object_data(self, **kwargs):
#             context = super().get_context_data(**kwargs)
#             # payload = Technician.get(...)
#             payload = "http://www.republiquedesmangues.fr/"
#             context["payload"] = payload
#             return context
        
