from fastapi import APIRouter, Request

from apis.v2.test_api.api import TestApiV2
from apis.v2.test_api.validator import TestApiV2Validator
from common.constants import NOT_FOUND_RESPONSE

# v2 router
v2_router = APIRouter(
    prefix='/sprdr_mw_apis/v2',
    tags=['v2'],
    responses=NOT_FOUND_RESPONSE
)


# v2 router paths
@v2_router.post('/test_api')
def test_api(request: Request, request_args: TestApiV2Validator):
    return TestApiV2(request=request, request_args=request_args).request_flow()
