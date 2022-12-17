from django.urls import path
from .views import ( RegisterEVIEW, RegisterPVIEW, LoginEVIEW, 
                     LoginPVIEW, ProfileVIEW, ChangeP_VIEW, 
                     SefcpVIEW, ResetP_VIEW, ActivateEmailVIEW, 
                     ActivatePhoneVIEW, Send2factorVIEW, Activate2factorVIEW )

urlpatterns = [
    path('register-email/', RegisterEVIEW.as_view(), name='registeremail'),
    path('register-phone/', RegisterPVIEW.as_view(), name='registerphone'),
    path('login-email/', LoginEVIEW.as_view(), name='loginemail'),
    path('login-phone/', LoginPVIEW.as_view(), name='loginphone'),
    path('profile/', ProfileVIEW.as_view(), name='profile'),
    path('cpv/', ChangeP_VIEW.as_view(), name='change-password'),
    path('sefcpv/', SefcpVIEW.as_view(), name='send-email'),
    path('reset-password/<uid>/<token>/', ResetP_VIEW.as_view(), name='reset-password'),
    path('activate/', ActivateEmailVIEW.as_view(), name='activate-user'),
    path('activate-phone/', ActivatePhoneVIEW.as_view(), name='activate-phone'),
    path('send2factor/', Send2factorVIEW.as_view(), name='send2factor'),
    path('activate2factor/', Activate2factorVIEW.as_view(), name='activate2factor')
]
