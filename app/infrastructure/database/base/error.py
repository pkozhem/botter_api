from fastapi import status
from pydantic import UUID4


class BaseError(Exception):
    def __init__(self, msg: str = "", code: int = status.HTTP_500_INTERNAL_SERVER_ERROR) -> None:
        self.msg: str = msg
        self.code: int = code

        super().__init__(msg)


class ObjectNotFoundError(BaseError):
    def __init__(self, id_: UUID4) -> None:
        super().__init__(
            msg=f"Object with {id_=} not found",
            code=status.HTTP_404_NOT_FOUND,
        )
