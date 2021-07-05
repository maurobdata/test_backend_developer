from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .lib.custom_status_code import map_code_to_message
from .lib.request_handler import get_generic_check_request
from .models import WebSite, SingleCheckRequest

from .serializers import WebSiteSerializer, WebSiteCheckRequestSerializer, SingleCheckRequestSerializer


class WebSiteViewSet(viewsets.ModelViewSet):
    queryset = WebSite.objects.all().order_by('-created_at')
    serializer_class = WebSiteSerializer
    # permission_classes = [permissions.IsAuthenticated]


@api_view(['GET', 'POST'])
def web_site_check_request(request, web_site_id):
    web_site = get_object_or_404(WebSite, pk=web_site_id)
    """Return all web site check requests for existing web site, or create a new one."""
    if request.method == 'GET':
        check_requests = web_site.websitecheckrequest_set.all()
        serializer = WebSiteCheckRequestSerializer(check_requests, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        request.data['url'] = web_site.url
        data_check_request = get_generic_check_request(request.data)
        check_request = web_site.websitecheckrequest_set.create(**data_check_request)
        serializer = WebSiteCheckRequestSerializer(instance=check_request, data=data_check_request)
        if serializer.is_valid():
            code_context = map_code_to_message(data_check_request.get('status_code'))
            if code_context['res'] == 'Success':
                web_site.n_requests_success += 1
            elif code_context['res'] == 'Warning':
                web_site.n_requests_warning += 1
            elif code_context['res'] == 'Fail':
                web_site.n_requests_fail += 1
            web_site.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleCheckRequestViewSet(viewsets.ModelViewSet):
    queryset = SingleCheckRequest.objects.all().order_by('-created_at')
    serializer_class = SingleCheckRequestSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Return all single check requests, or create a new one."""
        url = request.data.get('url')
        data_check_request = get_generic_check_request(request.data)
        data_check_request['url'] = url
        check_request = SingleCheckRequest(**data_check_request)
        serializer = SingleCheckRequestSerializer(instance=check_request, data=data_check_request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
