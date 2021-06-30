import pytest
# from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import UrlUnderInvestigation
from .views import OPTIONS
import datetime


# Create your tests here.
def create_url_under_investigation():
    uui = UrlUnderInvestigation(
        mnemonic_name="Example Domain",
        url="https://example.com/",
        regular_expression=".*",
        note="test",
        requests_successfully=0,
        requests_failed=0,
        requests_warning=0,
        favourite=False,
    )
    uui.save()
    return uui


def create_investigation(uui, start_time):
    investigation = uui.investigation_set.create(
        request_start_time=start_time,
        status_code=200
    )
    uui.save()
    investigation.save()
    return investigation


class UrlAnalysersModelTests(TestCase):
    @pytest.mark.unit
    def test_model_url_under_investigation(self):
        """Test Model UrlUnderInvestigation"""
        uui = create_url_under_investigation()

        assert uui.mnemonic_name == "Example Domain"
        assert uui.url == "https://example.com/"
        assert uui.regular_expression == ".*"
        assert uui.note == "test"
        assert uui.requests_successfully == 0
        assert uui.requests_failed == 0
        assert uui.requests_warning == 0
        assert uui.favourite is False

        assert repr(uui) == '<UrlUnderInvestigation: Url Under Investigation: \n' \
                            ' Example Domain \n' \
                            'https://example.com/ \n' \
                            '.* \n' \
                            'test \n' \
                            '0 \n' \
                            '0 \n' \
                            '0 \n' \
                            'False \n>'

    @pytest.mark.unit
    def test_model_investigatio(self):
        """Test Model Investigation"""
        time = datetime.datetime.utcnow()
        uui = create_url_under_investigation()
        investigation = create_investigation(uui, time)

        assert investigation.request_start_time == time
        assert investigation.request_end_time is None
        assert investigation.head is None
        assert investigation.body is None
        assert investigation.info is None
        assert investigation.status_code == 200

        assert repr(investigation) == '<Investigation: Url Under Investigation: \n Url Under Investigation: \n ' \
                                      'Example Domain \nhttps://example.com/ \n.* \ntest \n0 \n0 \n0 \nFalse \n ' \
                                      f'\n{time} \n' \
                                      f'None \nNone \nNone \nNone \n200 \n>'


class UrlAnalysersViewIndexTests(TestCase):
    @pytest.mark.unit
    def test_no_uui_index(self):
        """If no uui, respond with message."""
        response = self.client.get(reverse('url_analysers:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Analysis Available.")
        self.assertQuerysetEqual(response.context['uui_list'], [])

    @pytest.mark.unit
    def test_one_uui(self):
        """uui_list may also contain a single uui"""
        uui = create_url_under_investigation()
        response = self.client.get(reverse('url_analysers:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['uui_list'], [uui])

    @pytest.mark.unit
    def test_two_uui(self):
        """uui_list may also contain multiple uui"""
        uui = create_url_under_investigation()
        second_uui = create_url_under_investigation()
        response = self.client.get(reverse('url_analysers:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['uui_list'], [uui, second_uui], ordered=False)


class UrlAnalysersDetailViewTests(TestCase):
    @pytest.mark.unit
    def test_invalid_uui(self):
        """If uui.id is not valid, respond 404."""
        url = reverse('url_analysers:detail', args=(0,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @pytest.mark.unit
    def test_valid_uui(self):
        """uui Detail Happy path."""
        uui = create_url_under_investigation()
        response = self.client.get(reverse('url_analysers:detail', args=(uui.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['uui'], uui)
        self.assertEqual(response.context['options'], OPTIONS)


class UrlAnalysersInvestigationDetailViewTests(TestCase):
    # def setUp(self):
    #     self.patcher = patch('url_analysers.lib.custom_status_code.map_code_to_message')
    #     self.mock_foo = self.patcher.start()

    @pytest.mark.unit
    def test_invalid_investigation(self):
        """If uui.id is not valid, respond 404."""
        url = reverse('url_analysers:request', args=(0, 0))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # @patch('url_analysers.lib.custom_status_code.map_code_to_message', return_value={'message': message,
    #                                                                                  'res': 'Success'})
    # def test_valid_investigation(self, mock_map_code_to_message):
    @pytest.mark.unit
    def test_valid_investigation(self):
        """Investigation Happy path."""
        # import pdb;pdb.set_trace()

        # with patch('url_analysers.lib.custom_status_code.map_code_to_message') as mock_map_code_to_message:
        time = datetime.datetime.utcnow()
        uui = create_url_under_investigation()
        investigation = create_investigation(uui, time)
        response = self.client.get(reverse('url_analysers:request', args=(uui.id, investigation.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['investigation'], investigation)
        self.assertEqual(response.context['options'], OPTIONS)
        self.assertEqual(response.context['res'], 'Success')
        self.assertEqual(response.context['message'], 'This shows that the request was successful')

        # self.assertEqual(mock_map_code_to_message.called, 1)

    @pytest.mark.unit
    def test_invalid_investigation(self):
        """If uui.id is not valid, respond 404."""
        url = reverse('url_analysers:request', args=(0, 0))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)