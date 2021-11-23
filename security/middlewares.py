from app import app
from fastapi import Request

from common.constants import SUCCESS_STATUS_CODES

"""
Middlewares will be executed from bottom to top
"""


@app.middleware('http')
async def encrypt(request: Request, call_next):
    response = await call_next(request)
    if response.status_code in SUCCESS_STATUS_CODES:
        pass
    return response


@app.middleware('http')
async def decrypt(request: Request, call_next):
    request = request
    response = await call_next(request)
    return response


@app.middleware('http')
async def authenticate(request: Request, call_next):
    request = request
    response = await call_next(request)
    return response


@app.middleware('http')
async def not_found_404(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        # not_found_response = {
        #     'success': False,
        #     'message': '404 Not Found',
        #     'status_code': 404
        # }
        # raise HTTPException(status_code=404, detail=not_found_response)
        pass
    return response
