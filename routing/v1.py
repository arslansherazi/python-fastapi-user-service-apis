from fastapi import APIRouter, Request

from apis.v1.test_api.api import TestApi
from apis.v1.test_api.validator import TestApiValidator
from common.constants import NOT_FOUND_RESPONSE

# v1 router
v1_router = APIRouter(
    prefix='/sprdr_mw_apis/v1',
    tags=['v1'],
    responses=NOT_FOUND_RESPONSE
)


# v1 router paths
@v1_router.post('/test_api')
def test_api(request: Request, request_args: TestApiValidator):
    return TestApi(request=request, request_args=request_args).request_flow()
