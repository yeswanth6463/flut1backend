


from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('sailorslist/',views.sailorusersdetails.as_view(), name='sailors-list method no '),
    path('usercreation/',views.send_verification_email, name='user-creation method  post '),
    path('sailoremails/',views.sailorlist.as_view(),name="sailor email method no"),
    path('sailorform/',views.create_sailor,name="sailor form method post"),
    
    

    
    
]