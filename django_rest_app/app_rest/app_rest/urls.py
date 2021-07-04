"""app_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from rest_framework import routers
# from app_rest.user import views
from web_site_availability import views

# router = routers.DefaultRouter()
# router.register(r'sites', views.web_site, basename='Sites')
# router.register(r'site_check_requests/<int:web_site_id>/', views.web_site_check_request, basename='SiteCheckRequests')
# router.register(r'check_requests', views.single_check_request, basename='CheckRequests')
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),
    path('sites/', views.web_site, name='sites'),
    path('sites/<int:web_site_id>/requests/', views.web_site_check_request, name='sites_requests'),
    path('check_requests/', views.single_check_request, name='check_requests'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]
