from logging import getLogger

from litestar import Request, Response
from litestar.exceptions import (
	HTTPException,
	NotFoundException,
	ValidationException,
)
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

logger = getLogger(__name__)


def http_exception_handler(
	request: Request,
	exception: HTTPException,
) -> Response:
	status_code = getattr(
		exception,
		"status_code",
		HTTP_500_INTERNAL_SERVER_ERROR,
	)
	request.logger.error(f"{exception=}")
	request.logger.error(f"{request.method=}")
	request.logger.error(f"{request.url=}")
	request.logger.error(f"{request.query_params=}")

	detail = getattr(exception, "detail", "")
	extra = getattr(exception, "extra", "")

	return Response(
		content={
			"path": request.url.path,
			"detail": detail,
			"method": request.method,
			"extra": extra,
		},
		status_code=status_code,
	)


def not_found_exception_handler(
	request: Request,
	exception: NotFoundException,
) -> Response:
	status_code = getattr(exception, "status_code")
	request.logger.error(f"{exception=}")
	request.logger.error(f"{request.method=}")
	request.logger.error(f"{request.url=}")
	request.logger.error(f"{request.query_params=}")

	return Response(
		content={
			"path": request.url.path,
			"method": request.method,
		},
		status_code=status_code,
	)


def validation_exception_handler(
	request: Request,
	exception: ValidationException,
) -> Response:
	status_code = getattr(exception, "status_code")
	request.logger.error(f"{exception=}")
	request.logger.error(f"{request.url=}")
	request.logger.error(f"{request.query_params=}")

	detail = getattr(exception, "detail", "")
	extra = getattr(exception, "extra", "")
	request.logger.error(f"{detail=}")
	request.logger.error(f"{extra=}")

	return Response(
		content={
			"path": request.url.path,
			"detail": detail,
			"method": request.method,
			"extra": extra,
		},
		status_code=status_code,
	)
