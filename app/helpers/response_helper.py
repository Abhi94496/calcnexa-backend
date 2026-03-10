from typing import Any, Optional


class ResponseHelper:

    @staticmethod
    def success(
        message: str = "Success",
        data: Optional[Any] = None,
        status_code: int = 200
    ):
        return {
            "status": "success",
            "status_code": status_code,
            "message": message,
            "data": data
        }

    @staticmethod
    def error(
        message: str = "Something went wrong",
        error_type: str = "BAD_REQUEST",
        status_code: int = 400,
        details: Optional[Any] = None
    ):
        return {
            "status": "error",
            "status_code": status_code,
            "error_type": error_type,
            "message": message,
            "details": details
        }