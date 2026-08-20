from fastapi import Request
from fastapi.responses import JSONResponse

from frankfurter.exceptions import FrankfurterException


async def frankfurter_exception_handler(request: Request, exc: FrankfurterException):
    return JSONResponse(status_code=503, content={"detail": str(exc)})