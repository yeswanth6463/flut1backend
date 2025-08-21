


from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('sailorslist/',views.sailorusersdetails.as_view(), name='sailors-list method no '),
     path("register/", views.register_user, name="register_user"),
     path("verify/<str:token>/", views.verify_user, name="verify_user"),
    path('sailoremails/',views.sailorlist.as_view(),name="sailor email method no"),
    path('sailorform/',views.create_sailor,name="sailor form method post"),
    path('login/',views.login_for_user, name="login_for_user"),
    
    

    
    
]