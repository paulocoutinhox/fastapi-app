from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from models.web_response import WebResponse


def _process_validation_errors(exc: RequestValidationError) -> dict:
    errors = {}
    print(exc)

    for error in exc.errors():
        # extract field name from location path
        field_path = error["loc"]

        # handle different location patterns
        if len(field_path) > 1 and field_path[0] == "body":
            # body.field1.field2 -> field1.field2
            field_name = ".".join(str(loc) for loc in field_path[1:])
        elif len(field_path) > 1 and field_path[0] == "query":
            # query.param_name -> param_name
            field_name = field_path[1]
        elif len(field_path) > 1 and field_path[0] == "path":
            # path.param_name -> param_name
            field_name = field_path[1]
        elif len(field_path) > 1 and field_path[0] == "header":
            # header.header_name -> header_name
            field_name = field_path[1]
        elif len(field_path) > 1 and field_path[0] == "cookie":
            # cookie.cookie_name -> cookie_name
            field_name = field_path[1]
        else:
            # fallback: join all location parts
            field_name = ".".join(str(loc) for loc in field_path)

        message = error["msg"]

        # group errors by field name
        if field_name not in errors:
            errors[field_name] = []
        errors[field_name].append(message)

    return errors


async def _validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = _process_validation_errors(exc)

    return JSONResponse(
        status_code=422,
        content=WebResponse.e("validation-error", errors=errors).response.model_dump(),
    )


def setup(app):
    app.add_exception_handler(RequestValidationError, _validation_exception_handler)
