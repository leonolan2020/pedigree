from django.urls import path
from . import views
from .apps import APP_NAME

app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name='home'),
    path('Person_detail/<int:pk>/',views.PersonView().Person_detail,name='Person_detail'),
    
]
