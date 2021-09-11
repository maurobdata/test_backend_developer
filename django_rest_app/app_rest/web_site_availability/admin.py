"""Django administrator is available at http://.../admin/ """
from django.contrib import admin

from .models import SingleCheckRequest, WebSite, WebSiteCheckRequest

admin.site.register(WebSite)
admin.site.register(WebSiteCheckRequest)
admin.site.register(SingleCheckRequest)
