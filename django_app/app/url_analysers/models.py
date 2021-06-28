from django.db import models


class UrlUnderInvestigation(models.Model):
    mnemonic_name = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=200)
    regular_expression = models.CharField(max_length=200, null=True)
    note = models.CharField(max_length=200, null=True)
    requests_successfully = models.IntegerField(default=0)
    requests_failed = models.IntegerField(default=0)
    requests_warning = models.IntegerField(default=0)
    favourite = models.BooleanField(default=False)


class Investigation(models.Model):
    url_under_investigation = models.ForeignKey(UrlUnderInvestigation, on_delete=models.CASCADE)
    # response_time = request_end_time - request_start_time
    request_start_time = models.DateField()
    request_end_time = models.DateField(null=True)
    head = models.CharField(max_length=200, null=True)
    body = models.CharField(max_length=800, null=True)
    info = models.CharField(max_length=200, null=True)
    status_code = models.IntegerField(null=True)
