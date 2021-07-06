from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .lib.custom_status_code import map_code_to_message
from .lib.request_handler import get_generic_check_request
from .models import WebSite, SingleCheckRequest

from .serializers import WebSiteSerializer, WebSiteCheckRequestSerializer, SingleCheckRequestSerializer


class WebSiteViewSet(viewsets.ModelViewSet):
    """
    The WebSite allows you to save a url to make multiple requests.
    Url is required, other fields are for your pleasure.
    You could use this if you're on the fence ;)

    {"url": "[https://maieuticallabs.it/lavora-con-noi/](https://maieuticallabs.it/lavora-con-noi/)"}

    Then insert the id received to your url and navigate to:
    [https://test-backend-developer.herokuapp.com/sites/insert_id_here/requests/](https://test-backend-developer.herokuapp.com/sites/1/requests/)"""
    queryset = WebSite.objects.all().order_by('-created_at')
    serializer_class = WebSiteSerializer


@api_view(['GET', 'POST'])
def web_site_check_request(request, web_site_id):
    """
    Make as many Check Requests as you want to the url of this
    WebSite by clicking on the POST button. Optionally add
    search options with {"regular_expression": "insert_regex_here"}.
    (create here: [https://regex101.com/](https://regex101.com/))
    """

    web_site = get_object_or_404(WebSite, pk=web_site_id)
    if request.method == 'GET':
        check_requests = web_site.websitecheckrequest_set.all()
        serializer = WebSiteCheckRequestSerializer(check_requests, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        mutable_request_data = request.data.copy()
        mutable_request_data['url'] = web_site.url
        data_check_request = get_generic_check_request(mutable_request_data)
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
    """
    Make control requests with [https://docs.python-requests.org/en/master/](https://docs.python-requests.org/en/master/)
    by entering the url to contact and a regular expression (optional).
    For example you could try ;)

    {
        "url": "[https://maieuticallabs.it/lavora-con-noi/](https://maieuticallabs.it/lavora-con-noi/)",
        "regular_expression": "/*Yes, I can"
    }
    """
    queryset = SingleCheckRequest.objects.all().order_by('-created_at')
    serializer_class = SingleCheckRequestSerializer

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
