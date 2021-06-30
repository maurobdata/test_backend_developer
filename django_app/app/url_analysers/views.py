from urllib import request as u_request

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .lib.custom_status_code import map_code_to_message
from .models import UrlUnderInvestigation, Investigation

from django.http import HttpResponse, HttpResponseRedirect

OPTIONS = ['BASIC']


def index(request):
    uui_list = UrlUnderInvestigation.objects.all()
    context = {'uui_list': uui_list}
    return render(request, 'url_analysers/index.html', context)


def detail(request, uuid):
    uui = get_object_or_404(UrlUnderInvestigation, pk=uuid)
    context = {'uui': uui, 'options': OPTIONS}
    return render(request, 'url_analysers/detail.html', context)


def investigation_detail(request, uuid, investigation_id):
    investigation = get_object_or_404(Investigation, pk=investigation_id)
    code_context = map_code_to_message(investigation.status_code)
    context = {'investigation': investigation,
               'options': OPTIONS,
               'res': code_context['res'],
               'message': code_context['message']}
    return render(request, 'url_analysers/investigation_detail.html', context)


def investigate(request, uuid):
    uui = get_object_or_404(UrlUnderInvestigation, pk=uuid)
    start_time = timezone.now()
    investigation = uui.investigation_set.create(request_start_time=start_time)
    try:
        req = u_request.urlopen(uui.url)
    except BaseException as error:
        # Redisplay the uui detail form to perform a new request.
        investigation.request_end_time = timezone.now()
        uui.requests_failed += 1
        uui.save()
        investigation.save()
        context = {'uui': uui,
                   'options': OPTIONS,
                   'error_message': "An exception occurred: {}".format(error)}
        return render(request, 'url_analysers/detail.html', context)
    else:
        investigation.request_end_time = timezone.now()
        investigation.info = req.info()
        status_code = req.getcode()
        investigation.status_code = status_code
        code_context = map_code_to_message(status_code)
        if code_context['res'] == 'Success':
            uui.requests_successfully += 1
        elif code_context['res'] == 'Warning':
            uui.requests_warning += 1
        elif code_context['res'] == 'Fail':
            uui.requests_failed += 1
        uui.save()
        investigation.save()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('url_analysers:request', args=(uui.id, investigation.id)))
