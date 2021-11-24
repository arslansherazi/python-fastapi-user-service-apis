from fastapi import APIRouter, Request

from apis.v1.signup.api import Signup
from apis.v1.signup.validator import SignupApiValidator
from common.constants import NOT_FOUND_RESPONSE

# v1 router
v1_router = APIRouter(
    prefix='/sprdr_mw_apis/u_srvc/v1',
    tags=['v1'],
    responses=NOT_FOUND_RESPONSE
)


# v1 router paths
@v1_router.post('/signup')
def test_api(request: Request, request_args: SignupApiValidator):
    return Signup(request=request, request_args=request_args).request_flow()
