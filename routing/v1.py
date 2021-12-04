from fastapi import APIRouter, Request, Depends

from apis.v1.login.api import Login
from apis.v1.login.validator import LoginApiValidator
from apis.v1.signup.api import Signup
from apis.v1.signup.validator import SignupApiValidator
from common.constants import NOT_FOUND_RESPONSE, UNAUTHORIZED_REQUEST_RESPONSE, BAD_TOKEN_RESPONSE
from security.authentication import basic_auth_authentication, jwt_authentication

# v1 router
v1_router = APIRouter(
    prefix='/sprdr_mw_apis/u_srvc/v1',
    tags=['v1'],
    responses=NOT_FOUND_RESPONSE
)


# v1 router paths
@v1_router.post('/signup')
async def signup_api(
        request_args: SignupApiValidator, request: Request, is_authenticated: bool = Depends(basic_auth_authentication)
):
    if not is_authenticated:
        return UNAUTHORIZED_REQUEST_RESPONSE
    response = await Signup(request=request, request_args=request_args).request_flow()
    return response


# v1 router paths
@v1_router.post('/login')
async def login_api(
        request_args: LoginApiValidator, request: Request, is_authenticated: bool = Depends(basic_auth_authentication)
):
    if not is_authenticated:
        return UNAUTHORIZED_REQUEST_RESPONSE
    response = await Login(request=request, request_args=request_args).request_flow()
    return response
