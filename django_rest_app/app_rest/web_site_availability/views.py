from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, RegexValidator
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
    def web_site(self, request):
        """Return all web sites, or create a new one."""
        if request.method == 'GET':
            web_sites = self.queryset
            serializer = self.serializer_class(web_sites, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            url = request.data.get('url')
            try:
                validator = URLValidator()
                validator(url)
            except ValidationError as url_error:
                return Response(url_error, status=status.HTTP_400_BAD_REQUEST)
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
        regular_expression = request.data.get('regular_expression')
        if regular_expression:
            try:
                validator = RegexValidator()
                validator(regular_expression)
            except ValidationError as reg_error:
                return Response(reg_error, status=status.HTTP_400_BAD_REQUEST)

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
    url_validator = URLValidator()
    reg_validator = RegexValidator()

    # permission_classes = [permissions.IsAuthenticated]

    @api_view(['GET', 'POST'])
    def single_check_request(self, request):
        """Return all single check requests, or create a new one."""
        if request.method == 'GET':
            check_requests = self.queryset
            serializer = self.serializer_class(check_requests, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            url = request.data.get('url')
            try:
                self.url_validator(url)
            except ValidationError as url_error:
                return Response(url_error, status=status.HTTP_400_BAD_REQUEST)
            regular_expression = request.data.get('regular_expression')
            if regular_expression:
                try:
                    self.reg_validator(regular_expression)
                except ValidationError as reg_error:
                    return Response(reg_error, status=status.HTTP_400_BAD_REQUEST)

            data_check_request = get_generic_check_request(request.data)
            data_check_request['url'] = url
            check_request = SingleCheckRequest(**data_check_request)
            serializer = SingleCheckRequestSerializer(instance=check_request, data=data_check_request)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
