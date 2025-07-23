class BaseRepoException(Exception):
    detail = "Internal server error"

    def __init__(self, *args):
        super().__init__(self.detail, *args)


class ObjectNotFoundRepoException(BaseRepoException):
    detail = "Object not found"


class CannotAddObjectRepoException(BaseRepoException):
    detail = "Cannot add object"
