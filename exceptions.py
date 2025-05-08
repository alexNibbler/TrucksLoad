class LoadingException(Exception):
    def __init__(self, message: str = None, reason: str = None):
        super().__init__(message)
        self.message = message
        self.reason = reason

    def __str__(self):
        details = [f"Message: {self.message}"]
        if self.reason:
            details.append(self.reason)
        return " | ".join(details)


class NotEnoughPackages(LoadingException):
    def __init__(self):
        super().__init__(message = "The packages cannot load any available truck to at least 80%.")


class TooManyPackages(LoadingException):
    def __init__(self):
        super().__init__(message = "The packages cannot fit any available truck")


class TooBigPackages(LoadingException):
    def __init__(self):
        super().__init__(message = f"The packages are too big to fit any available truck.")