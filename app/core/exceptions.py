class DomainException(Exception):
    """Base class for all domain-level exceptions. Routers translate these
    to HTTP responses at the boundary — services should never raise
    HTTPException directly."""

    message: str = "An unexpected error occurred."

    def __init__(self, message: str | None = None):
        if message:
            self.message = message
        super().__init__(self.message)

class TripNotFoundError(DomainException):
    message = "Trip not found."

class UserNotFoundError(DomainException):
    message = "User not found."

class TripLimitsNotSetError(DomainException):
    message = "Trip limits have not been set."

class UserNotInTripError(DomainException):
    message = "User is not a member of this trip."

class InvalidTripLimitsError(DomainException):
    message = "Trip limits must include exactly one entry per category."