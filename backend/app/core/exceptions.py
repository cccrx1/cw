from fastapi import HTTPException, status


class PetManagementException(HTTPException):
    def __init__(self, code: int, message: str):
        super().__init__(
            status_code=status.HTTP_200_OK,
            detail={
                "code": code,
                "message": message,
                "data": None
            }
        )


class ValidationError(PetManagementException):
    def __init__(self, message: str):
        super().__init__(code=40001, message=message)


class UnauthorizedError(PetManagementException):
    def __init__(self, message: str = "未登录或Token无效"):
        super().__init__(code=40002, message=message)


class ForbiddenError(PetManagementException):
    def __init__(self, message: str = "无权限访问"):
        super().__init__(code=40003, message=message)


class NotFoundError(PetManagementException):
    def __init__(self, message: str = "资源不存在"):
        super().__init__(code=40004, message=message)


class RateLimitError(PetManagementException):
    def __init__(self, message: str = "请求过于频繁"):
        super().__init__(code=40009, message=message)


class InternalError(PetManagementException):
    def __init__(self, message: str = "服务内部错误"):
        super().__init__(code=50001, message=message)


class DifyError(PetManagementException):
    def __init__(self, message: str = "Dify服务调用失败"):
        super().__init__(code=50010, message=message)