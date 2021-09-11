""""""
from datetime import datetime

import pytest
from django.test import TestCase
from freezegun import freeze_time

from .models import WebSite


def create_web_site():
    web_site = WebSite(
        mnemonic_name="Example Domain",
        url="https://example.com/",
        note="test",
        n_requests_success=0,
        n_requests_fail=0,
        n_requests_warning=0,
    )
    web_site.save()
    return web_site


def create_web_site_check_request(web_site, start_time):
    check_request = web_site.websitecheckrequest_set.create(
        created_at=start_time,
    )
    web_site.save()
    check_request.save()
    return check_request


class UrlAnalysersModelTests(TestCase):
    @pytest.mark.unit
    def test_create_web_site(self):
        """Test Model WebSite"""
        web_site = create_web_site()

        assert web_site.mnemonic_name == "Example Domain"
        assert web_site.url == "https://example.com/"
        assert web_site.note == "test"
        assert web_site.n_requests_success == 0
        assert web_site.n_requests_fail == 0
        assert web_site.n_requests_warning == 0

    @pytest.mark.unit
    def test_create_web_site_check_request(self):
        """Test Model WebSiteCheckRequest"""
        time = datetime.utcnow()
        web_site = create_web_site()
        check_request = create_web_site_check_request(web_site, time)
        assert check_request.url_web_site == web_site


class WebSiteViewSetTests(TestCase):
    @pytest.mark.unit
    def test_no_web_site(self):
        """If no web site, respond with empty response."""
        response = self.client.get("/sites/")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context)

    @pytest.mark.unit
    @freeze_time("2011-09-11T00:00:00Z", as_kwarg="frozen_time")
    def test_one_web_site(self, frozen_time):
        """/sites/ may also contain a single web site"""
        dj_format = "%Y-%m-%dT%H:%M:%SZ"
        time = frozen_time.time_to_freeze.date().strftime(dj_format)
        web_site = create_web_site()
        response = self.client.get("/sites/")

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "created_at": time,
                        "updated_at": time,
                        "url": web_site.url,
                        "mnemonic_name": web_site.mnemonic_name,
                        "note": web_site.note,
                        "n_requests_success": web_site.n_requests_success,
                        "n_requests_fail": web_site.n_requests_fail,
                        "n_requests_warning": web_site.n_requests_warning,
                    }
                ],
            },
        )


class InvalidRequestViewSetTests(TestCase):
    @pytest.mark.unit
    def test_invalid_web_site_id(self):
        """If web_site.id is not valid, respond 404."""
        response = self.client.get("/sites/0/")
        self.assertEqual(response.status_code, 404)

    @pytest.mark.unit
    def test_invalid_single_check_request_id(self):
        """If check_requests.id is not valid, respond 404."""
        response = self.client.get("/check_requests/1/")
        self.assertEqual(response.status_code, 404)

    @pytest.mark.unit
    def test_invalid_url(self):
        """If url is not registered, respond 404."""
        response = self.client.get("/impossible_url/")
        self.assertEqual(response.status_code, 404)


class SingleCheckRequestViewSetTests(TestCase):
    @pytest.mark.unit
    @freeze_time("1914-07-28T00:00:00Z", as_kwarg="frozen_time")
    def test_get_web_site_check_request(self, frozen_time):
        """Web Site Check Request Happy path get."""
        dj_format = "%Y-%m-%dT%H:%M:%SZ"
        time = frozen_time.time_to_freeze.date().strftime(dj_format)
        web_site = create_web_site()
        check_request = create_web_site_check_request(web_site, time)
        response = self.client.get("/sites/1/requests/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": 1,
                    "created_at": time,
                    "updated_at": time,
                    "response_time": None,
                    "status_code": None,
                    "response": None,
                    "regular_expression": None,
                    "match_regular_expression": None,
                    "pattern_regular_expression": None,
                    "lib_request_type": None,
                    "url_web_site": 1,
                }
            ],
        )

    @pytest.mark.unit
    @freeze_time("2914-07-28T00:00:00Z", as_kwarg="frozen_time")
    def test_post_web_site_check_request_no_params(self, frozen_time):
        """Web Site Check Request Happy path post."""
        dj_format = "%Y-%m-%dT%H:%M:%SZ"
        time = frozen_time.time_to_freeze.date().strftime(dj_format)
        web_site = create_web_site()
        check_request = create_web_site_check_request(web_site, time)
        response = self.client.post("/sites/1/requests/")

        self.assertEqual(response.status_code, 201)

    @pytest.mark.unit
    @freeze_time("2914-07-28T00:00:00Z", as_kwarg="frozen_time")
    def test_post_web_site_check_request(self, frozen_time):
        """Web Site Check Request Happy path post."""
        dj_format = "%Y-%m-%dT%H:%M:%SZ"
        time = frozen_time.time_to_freeze.date().strftime(dj_format)
        web_site = create_web_site()
        check_request = create_web_site_check_request(web_site, time)
        response = self.client.post(
            "/sites/1/requests/", {"url": "https://www.google.com/"}
        )

        self.assertEqual(response.status_code, 201)
