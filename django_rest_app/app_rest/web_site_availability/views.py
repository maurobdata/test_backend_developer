from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.decorators import api_view

from rest_framework.response import Response

from .lib.request_handler import get_generic_check_request
from .models import WebSite, SingleCheckRequest

from .serializers import WebSiteSerializer, WebSiteCheckRequestSerializer, SingleCheckRequestSerializer


@api_view(['GET', 'POST'])
def web_site(request):
    """Return all web sites, or create a new one."""
    if request.method == 'GET':
        web_sites = WebSite.objects.all()
        serializer = WebSiteSerializer(web_sites, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = WebSiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def single_check_request(request):
    """Return all single check requests, or create a new one."""
    if request.method == 'GET':
        check_requests = SingleCheckRequest.objects.all()
        serializer = SingleCheckRequestSerializer(check_requests, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        url = request.data.get('url')
        data_check_request = get_generic_check_request(request.data)
        data_check_request['url'] = url
        check_request = SingleCheckRequest(**data_check_request)
        serializer = SingleCheckRequestSerializer(instance=check_request, data=data_check_request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
