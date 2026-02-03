from typing import Any

from fastapi import HTTPException, status

from utils.error_code import ERROR_CODE


def get_error_msg(
    error_code: int, extra_info: str | None, *arg: str | None
) -> dict[str, str] | None:
    if error_code not in ERROR_CODE:
        return None

    error_msg = ERROR_CODE[error_code]
    error_msg["error_code"] = str(error_code)
    if "message" in error_msg.keys():
        template_msg = error_msg["message"]

        try:
            error_msg["message"] = template_msg.format(*arg)
        except IndexError:
            error_msg["message"] = template_msg

        if extra_info:
            error_msg["info"] = extra_info
    return error_msg


class ErrorException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        error_code: Any = None,
        error_args: list[Any] = [],
        error_info: Any = None,
    ) -> None:
        if not error_code:
            error_code = self.status_code

        self.error_code = error_code

        detail = get_error_msg(error_code, error_info, *error_args)
        super().__init__(status_code=self.status_code, detail=detail)


# Details
class Unauthorized(ErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED


class NotAcceptable(ErrorException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class BadRequest(ErrorException):
    status_code = status.HTTP_400_BAD_REQUEST


class Forbidden(ErrorException):
    status_code = status.HTTP_403_FORBIDDEN


class NotFound(ErrorException):
    status_code = status.HTTP_404_NOT_FOUND
