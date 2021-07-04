from django.core.validators import URLValidator, RegexValidator
from django.db import models


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    completed_at = models.DateTimeField(null=True, editable=False)

    class Meta:
        abstract = True


class WebSite(TimeStampMixin):
    # http://www.faqs.org/rfcs/rfc2616.html - unlimited theoretical
    # https://datatracker.ietf.org/doc/html/rfc7230#section-3.1.1 - suggestion
    # may_be_supported_url = models.TextField() - up to 2048 some support them
    url = models.CharField(max_length=200, validators=[URLValidator])

    mnemonic_name = models.CharField(max_length=200, null=True)
    note = models.CharField(max_length=200, null=True)
    n_requests_success = models.IntegerField(default=0, editable=False)
    n_requests_fail = models.IntegerField(default=0, editable=False)
    n_requests_warning = models.IntegerField(default=0, editable=False)
    favourite = models.BooleanField(null=True)

    def __str__(self):
        return f"Web Site: \n " \
               f"{self.url} \n" \
               f"{self.mnemonic_name} \n" \
               f"{self.note} \n" \
               f"{self.n_requests_success} \n" \
               f"{self.n_requests_fail} \n" \
               f"{self.n_requests_warning} \n" \
               f"{self.favourite} \n"


class CheckRequest(TimeStampMixin):
    response_time = models.FloatField(null=True, editable=False)
    status_code = models.IntegerField(null=True, editable=False)
    response = models.TextField(max_length=100000, null=True, editable=False)
    regular_expression = models.CharField(max_length=200, null=True, validators=[RegexValidator])
    match_regular_expression = models.BooleanField(null=True, editable=False)
    lib_request_type = models.CharField(max_length=200, null=True, editable=False)

    class Meta:
        abstract = True


class WebSiteCheckRequest(CheckRequest):
    url_web_site = models.ForeignKey(WebSite, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return f"Web Site Check Request: \n " \
               f"{self.url_web_site} \n" \
               f"{self.response_time} \n" \
               f"{self.status_code} \n" \
               f"{self.regular_expression} \n" \
               f"{self.match_regular_expression} \n" \
               f"{self.lib_request_type} \n" \
               f"{self.response}"


class SingleCheckRequest(CheckRequest):
    url = models.CharField(max_length=200, validators=[URLValidator])

    def __str__(self):
        return f"Single Check Request: \n " \
               f"{self.url} \n" \
               f"{self.response_time} \n" \
               f"{self.status_code} \n" \
               f"{self.regular_expression} \n" \
               f"{self.match_regular_expression} \n" \
               f"{self.lib_request_type} \n" \
               f"{self.response} \n"
