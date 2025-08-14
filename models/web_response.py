from typing import Any, Dict, List, Optional, Union

from fastapi import Response, status
from pydantic import BaseModel, ConfigDict, ValidationError


class WebResponse(BaseModel):
    """
    Standard web service response class with common pattern
    """

    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def create(
        cls,
        success: bool,
        message: str = "",
        data: Optional[Union[Dict[str, Any], Any]] = None,
        errors: Optional[Dict[str, List[str]]] = None,
    ) -> "WebResponseBuilder":
        """
        Create a WebResponse with flexible data handling.

        Args:
            success: Whether the operation was successful
            message: Response message
            data: Data to include (can be dict, model, or any object)
            errors: Validation errors if any
        """
        # process data intelligently
        processed_data = cls._process_data(data, errors)

        # create response
        response = cls(success=success, message=message, data=processed_data)
        return WebResponseBuilder(response)

    @classmethod
    def s(
        cls,
        message: str = "success",
        data: Optional[Union[Dict[str, Any], Any]] = None,
    ) -> "WebResponseBuilder":
        """Create a success response"""
        return cls.create(True, message, data)

    @classmethod
    def e(
        cls,
        message: str = "error",
        data: Optional[Union[Dict[str, Any], Any]] = None,
        errors: Optional[Dict[str, List[str]]] = None,
        verror: Optional[ValidationError] = None,
    ) -> "WebResponseBuilder":
        """
        Create an error response

        Args:
            message: Error message
            data: Additional data to include
            errors: Manual validation errors dict
            verror: Pydantic ValidationError to process automatically
        """
        # if validation_error is provided, process it automatically
        if verror is not None:
            processed_errors = cls._process_validation_error(verror)
            # merge with manual errors if provided
            if errors:
                for field, field_errors in errors.items():
                    if field not in processed_errors:
                        processed_errors[field] = []
                    processed_errors[field].extend(field_errors)
            errors = processed_errors

        return cls.create(False, message, data, errors)

    @classmethod
    def _process_validation_error(
        cls, validation_error: ValidationError
    ) -> Dict[str, List[str]]:
        """
        Process Pydantic ValidationError and convert to standardized error format

        Args:
            validation_error: Pydantic ValidationError instance

        Returns:
            Dict with field names as keys and lists of error messages as values
        """
        errors = {}
        for error in validation_error.errors():
            # get field name from location
            field = error["loc"][0] if error["loc"] else "unknown"
            message = error["msg"]

            # initialize field if not exists
            if field not in errors:
                errors[field] = []

            # add error message
            errors[field].append(message)

        return errors

    @classmethod
    def _process_data(
        cls,
        data: Optional[Union[Dict[str, Any], Any]],
        errors: Optional[Dict[str, List[str]]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Process data intelligently, handling models and different types"""
        if data is None and errors is None:
            return None

        result = {}

        # handle errors
        if errors:
            result["errors"] = errors

        # handle data
        if data is not None:
            if isinstance(data, dict):
                # dict
                result.update(data)
            elif hasattr(data, "model_dump"):
                # pydantic model
                result.update(data.model_dump())
            elif hasattr(data, "to_dict"):
                # orm model
                result.update(data.to_dict())
            elif hasattr(data, "__dict__"):
                # regular object
                result.update(data.__dict__)
            else:
                # single value or other type
                result["value"] = data

        return result if result else None

    def add_data(self, key: str, value: Any) -> "WebResponse":
        """Add an item to the data field"""
        if self.data is None:
            self.data = {}
        self.data[key] = value
        return self

    def add_error(self, field: str, error_message: str) -> "WebResponse":
        """Add a validation error"""
        if self.data is None:
            self.data = {}
        if "errors" not in self.data:
            self.data["errors"] = {}
        if field not in self.data["errors"]:
            self.data["errors"][field] = []
        self.data["errors"][field].append(error_message)
        return self


class WebResponseBuilder:
    """Builder class for WebResponse with status code chaining"""

    def __init__(self, response: WebResponse):
        self.response = response

    def _to_response(self, status_code: int) -> Response:
        """Convert to FastAPI Response with status code"""
        return Response(
            content=self.response.model_dump_json(),
            media_type="application/json",
            status_code=status_code,
        )

    def ok(self) -> Response:
        """200 OK"""
        return self._to_response(status.HTTP_200_OK)

    def created(self) -> Response:
        """201 Created"""
        return self._to_response(status.HTTP_201_CREATED)

    def bad_request(self) -> Response:
        """400 Bad Request"""
        return self._to_response(status.HTTP_400_BAD_REQUEST)

    def unauthorized(self) -> Response:
        """401 Unauthorized"""
        return self._to_response(status.HTTP_401_UNAUTHORIZED)

    def forbidden(self) -> Response:
        """403 Forbidden"""
        return self._to_response(status.HTTP_403_FORBIDDEN)

    def not_found(self) -> Response:
        """404 Not Found"""
        return self._to_response(status.HTTP_404_NOT_FOUND)

    def conflict(self) -> Response:
        """409 Conflict"""
        return self._to_response(status.HTTP_409_CONFLICT)

    def unprocessable_entity(self) -> Response:
        """422 Unprocessable Entity"""
        return self._to_response(status.HTTP_422_UNPROCESSABLE_ENTITY)

    def internal_server_error(self) -> Response:
        """500 Internal Server Error"""
        return self._to_response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    def service_unavailable(self) -> Response:
        """503 Service Unavailable"""
        return self._to_response(status.HTTP_503_SERVICE_UNAVAILABLE)

    def r(self, status_code: int) -> Response:
        """Return with custom status code"""
        return self._to_response(status_code)

    def r200(self) -> Response:
        return self.ok()

    def r201(self) -> Response:
        return self.created()

    def r400(self) -> Response:
        return self.bad_request()

    def r401(self) -> Response:
        return self.unauthorized()

    def r403(self) -> Response:
        return self.forbidden()

    def r404(self) -> Response:
        return self.not_found()

    def r409(self) -> Response:
        return self.conflict()

    def r422(self) -> Response:
        return self.unprocessable_entity()

    def r500(self) -> Response:
        return self.internal_server_error()

    def r503(self) -> Response:
        return self.service_unavailable()
