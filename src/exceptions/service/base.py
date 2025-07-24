class BaseServiceException(Exception):
    detail = "Internal server error"

    def __init__(self, *args):
        super().__init__(self.detail, *args)
