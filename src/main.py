from typing import Annotated

from litestar import Litestar, get, post, Response, Request, put
from litestar.contrib.htmx.request import HTMXRequest
from asyncio import sleep
from litestar.contrib.htmx.response import HTMXTemplate
from litestar.template.config import TemplateConfig
from litestar.response import Template
from litestar.contrib.jinja import JinjaTemplateEngine
from rich import print
from pathlib import Path
from litestar.params import Body
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException, ValidationException
from dataclasses import dataclass
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR


def app_exception_handler(request: Request, exc: HTTPException) -> Response:
	status_code = getattr(exc, "status_code", HTTP_500_INTERNAL_SERVER_ERROR)
	detail = getattr(exc, "detail", "")
	print("app_exception_handler")
	print("detail")
	print(detail)
	return Response(
		content=detail,
		# content={
		# 	"error": "server error",
		# 	"path": request.url.path,
		# 	"detail": detail,
		# 	"status_code": exc.status_code,
		# },
		status_code=status_code,
	)


def app_exception_validation_error_handler(request: Request, exc: ValidationException) -> Response:
	print("app_exception_validation_error_handler")
	status_code = getattr(exc, "status_code", HTTP_500_INTERNAL_SERVER_ERROR)
	detail = getattr(exc, "detail", "")
	extra = getattr(exc, "extra", "")
	print(extra)
	print(detail)
	return Response(
		content=detail,
		# content={
		# 	"error": "server error",
		# 	"path": request.url.path,
		# 	"detail": detail,
		# 	"status_code": exc.status_code,
		# },
		status_code=status_code,
	)


@dataclass
class UserMessage:
	name: str
	email: str
	message: str


@get("/")
async def index() -> Template:
	return HTMXTemplate(template_name="index.html.jinja")


@post("/users/messages")
async def post_users_messages(
	data: Annotated[UserMessage | None, Body(media_type=RequestEncodingType.URL_ENCODED)],
) -> Template:
	await sleep(3)
	if data is None:  # Reset message
		HTMXTemplate(template_name="message.html.jinja", context={"user": UserMessage(name="", email="", message="")})
	return HTMXTemplate(template_name="message.html.jinja", context={"user": data})


app = Litestar(
	route_handlers=[index, post_users_messages],
	debug=True,
	request_class=HTMXRequest,
	template_config=TemplateConfig(directory=Path("src/templates"), engine=JinjaTemplateEngine),
	exception_handlers={HTTPException: app_exception_handler, ValidationException: app_exception_validation_error_handler},
)
