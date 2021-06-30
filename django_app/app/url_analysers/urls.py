from django.urls import path

from . import views

app_name = 'url_analysers'
urlpatterns = [
    # ex: /urls/
    path('', views.index, name='index'),
    # ex: /urls/5/
    path('<int:uuid>/', views.detail, name='detail'),
    # ex: /urls/5/requests/
    path('<int:uuid>/request/<int:investigation_id>/', views.investigation_detail, name='request'),
    # ex: /urls/5/spy/
    path('<int:uuid>/spy/', views.investigate, name='spy'),
]