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

    def __str__(self):
        return f"Url Under Investigation: \n " \
               f"{self.mnemonic_name} \n" \
               f"{self.url} \n" \
               f"{self.regular_expression} \n" \
               f"{self.note} \n" \
               f"{self.requests_successfully} \n" \
               f"{self.requests_warning} \n" \
               f"{self.requests_failed} \n" \
               f"{self.favourite} \n"


class Investigation(models.Model):
    url_under_investigation = models.ForeignKey(UrlUnderInvestigation, on_delete=models.CASCADE)
    # response_time = request_end_time - request_start_time
    request_start_time = models.DateField()
    request_end_time = models.DateField(null=True)
    head = models.CharField(max_length=200, null=True)
    body = models.CharField(max_length=800, null=True)
    info = models.CharField(max_length=200, null=True)
    status_code = models.IntegerField(null=True)

    def __str__(self):
        return f"Url Under Investigation: \n " \
               f"{self.url_under_investigation} \n" \
               f"{self.request_start_time} \n" \
               f"{self.request_end_time} \n" \
               f"{self.head} \n" \
               f"{self.body} \n" \
               f"{self.info} \n" \
               f"{self.status_code} \n"
