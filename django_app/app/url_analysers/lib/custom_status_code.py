SUCCESS = 'Success'
FAIL = 'Fail'
WARNING = 'Warning'


def _1xx():
    message = "This lets us know that the request was received"
    context = {'message': message, 'res': WARNING}
    return context


def _2xx():
    message = "This shows that the request was successful"
    context = {'message': message, 'res': SUCCESS}
    return context


def _3xx():
    message = "This is for redirects (temporary and permanent)"
    context = {'message': message, 'res': WARNING}
    return context


def _4xx():
    message = "Client errors"
    context = {'message': message, 'res': FAIL}
    return context


def _5xx():
    message = "Server errors"
    context = {'message': message, 'res': FAIL}
    return context


def map_code_to_message(status_code):
    """Mapper to convert status code to understandable message"""
    switcher = {
        '1': _1xx,
        '2': _2xx,
        '3': _3xx,
        '4': _4xx,
        '5': _5xx,
    }
    # First digit of integer code
    family = str(status_code)[0]
    # Get the function from switcher dictionary
    func = switcher.get(family, lambda: {'message': "Invalid http code", 'res': FAIL})
    # Execute the function
    return func()
