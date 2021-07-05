import re
import time

try:  # Try importing requests first
    import requests
except ImportError:
    try:  # Try importing Python3 urllib
        import urllib.request
    except AttributeError:  # Now importing Python2 urllib
        import urllib


def get_generic_check_request(data):
    result_data = {}
    # result_data['url'] = data.get('url')
    url = data.get('url')
    if not url:
        return
    try:  # Using requests
        request = requests.get(url)  # requests.models.Response
        result_data['lib_request_type'] = str((type(request)))
        result_data['response_time'] = request.elapsed.total_seconds()
        result_data['status_code'] = request.status_code
        result_data['response'] = request.text
    except NameError:
        try:  # Using Python3 urllib
            start = time.time()
            with urllib.request.urlopen(url) as response:
                request = response  # http.client.HTTPResponse
                page = request.read()
                end = time.time()
                request.close()
            result_data['lib_request_type'] = str((type(request)))
            result_data['response_time'] = end - start
            result_data['status_code'] = request.getcode()
            result_data['response'] = str(page)
        except AttributeError:  # Using Python3 urllib
            urllib.urlopen(url)  # Should raise correct Exception

    result_data['regular_expression'] = data.get('regular_expression')
    if result_data.get('regular_expression'):
        result_data['pattern_regular_expression'] = re.search(
            result_data.get('regular_expression'),
            result_data.get('response'))
        result_data['match_regular_expression'] = True if result_data.get(
            'pattern_regular_expression') else False
    return result_data
