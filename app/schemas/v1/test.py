from rest_framework.serializers import Serializer
from drf_spectacular.utils import extend_schema


class TestRequest(Serializer):
    pass


class TestResponse(Serializer):
    pass


test = {
    "test": extend_schema(
        summary="테스트 API", request=TestRequest, responses=TestResponse
    )
}