from datetime import datetime


class HttpException(Exception):
    status_code = 404

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.exception = type(self).__name__
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {'timestamp': datetime.now(), 'message': self.message, "exception": self.exception}


class StartDateHasToBeEarlierThenEndDate(HttpException):
    pass


class DatesShouldNotBeFromPast(HttpException):
    pass


class NotEnoughData(HttpException):
    pass
