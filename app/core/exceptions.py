from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, message: str, detail: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": message, "extra_info": detail}
        )


class InvalidOperation(Exception):
    def __init__(self, message: str, detail: str):
        self.message = message
        self.deatil = detail
        super.__init__(self.detail)


class PlanResolverError(Exception):
    pass
