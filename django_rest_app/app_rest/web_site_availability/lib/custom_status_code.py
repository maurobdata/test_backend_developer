"""Customize http status code"""
SUCCESS = "Success"
FAIL = "Fail"
WARNING = "Warning"
ERROR = "Error"
MORE_INFO = (
    "\n More info about HTTP Status Codes at: "
    "https://www.restapitutorial.com/httpstatuscodes.html \n"
    " RFC: https://datatracker.ietf.org/doc/html/rfc1945#section-6.1.1"
)


def _err():
    message_error = "Invalid http code"
    message_error += MORE_INFO
    error = {"message": message_error, "res": ERROR}
    return error


def _1xx():
    message = "This lets us know that the request was received"
    message += MORE_INFO
    context = {"message": message, "res": WARNING}
    return context


def _2xx():
    message = "This shows that the request was successful"
    message += MORE_INFO
    context = {"message": message, "res": SUCCESS}
    return context


def _3xx():
    message = "This is for redirects (temporary and permanent)"
    message += MORE_INFO
    context = {"message": message, "res": WARNING}
    return context


def _4xx():
    message = "Client errors"
    message += MORE_INFO
    context = {"message": message, "res": FAIL}
    return context


def _5xx():
    message = "Server errors"
    message += MORE_INFO
    context = {"message": message, "res": FAIL}
    return context


switcher = {
    "1": _1xx,
    "2": _2xx,
    "3": _3xx,
    "4": _4xx,
    "5": _5xx,
}


def map_code_to_message(status_code):
    """Mapper to convert status code to understandable message"""
    # RFC https://datatracker.ietf.org/doc/html/rfc1945#section-6.1.1
    # specify 3 digits letters
    if len(str(status_code)) != 3:
        # Execute the error
        return _err()
    # First digit of integer code
    family = str(status_code)[0]
    # Get the function from switcher dictionary
    func = switcher.get(family)
    # Execute the function
    return func()
