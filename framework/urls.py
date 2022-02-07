from django.urls import path
from . import views

app_name = 'framework'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    # path('api/login/', views.login , name='api-login'),
    path('missions/', views.MissionsView.as_view(), name='missions'),
    path('mission/<uuid:mission_uuid>/', views.MissionOverView.as_view(), name='mission_overview'),
    # path('pres/', views.presentation, name='presentation'),
    # path('scan/', views.scan_prompt, name='scan_prompt'),
    # path('scan/cam/', views.scan_cam, name='scan_cam'),
    path('mission/<uuid:mission_uuid>/terminal', views.TerminalOverview.as_view(), name='terminal_overview'),
    path('mission/<uuid:mission_uuid>/locker/<uuid:locker_uuid>', views.LockerDetails.as_view(), name='object'),
    path('mission/<uuid:mission_uuid>/locker/<uuid:locker_uuid>/error', views.ErrorPage.as_view(), name='error'),
    path('mission/qrcode', views.QRDisplay.as_view(), name='qr-code'),

]