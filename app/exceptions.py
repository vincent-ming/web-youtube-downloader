class WYDApiError(Exception):
    def __init__(self, message: str = 'Service is unavailable'):
        self.message = message
        super().__init__(message)


class VideoTooLongError(WYDApiError):
    """Exception raised when the video length exceeds the allowed limit."""
    def __init__(self, message="Video is too long"):
        super().__init__(message)


class InvalidUrlError(WYDApiError):
    """Exception raised when the url invalid."""
    def __init__(self, url):
        super().__init__('%s is invalid url' % url)


class InvalidVideoError(WYDApiError):
    """Exception raised when the video invalid."""
    def __init__(self, message):
        super().__init__(message)
