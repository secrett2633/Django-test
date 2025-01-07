from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view

from app.schemas.v1.test import test


@extend_schema_view(**test)
class TestSet(viewsets.ViewSet):
    """
    ViewSet for handling test operations.

    Attributes:
        serializer_class (Type[TestRequest]): Serializer class for request validation.
    """

    @action(detail=False, methods=["POST"])
    def test(self, request: Request) -> Response:
        """
        Test action.

        Args:
            request (Request): The incoming request object.

        Returns:
            Response: The response from the test_service.
        """
        return Response({"message": "Hello, World!"})