from asyncio import sleep
from dataclasses import dataclass
from logging import INFO, getLevelName
from pathlib import Path
from typing import Annotated

from litestar import Litestar, get, post
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.enums import RequestEncodingType
from litestar.exceptions import (
	HTTPException,
	NotFoundException,
	ValidationException,
)
from litestar.logging import LoggingConfig
from litestar.params import Body
from litestar.response import Template
from litestar.template.config import TemplateConfig

from src.exceptions import (
	http_exception_handler,
	not_found_exception_handler,
	validation_exception_handler,
)

logging_config = LoggingConfig(
	root={"level": getLevelName(INFO), "handlers": ["console"]},
	formatters={
		"standard": {"format": "%(levelname)s - %(name)s - %(message)s"},
	},
)


@dataclass
class UserMessage:
	name: str
	email: str
	message: str


@get("/")
async def index() -> Template:
	return HTMXTemplate(
		template_name="index.html.jinja",
		context={"user": UserMessage(name="", email="", message="")},
	)


@post("/users/messages")
async def post_users_messages(
	data: Annotated[
		UserMessage | None,
		Body(media_type=RequestEncodingType.URL_ENCODED),
	],
) -> Template:
	await sleep(2)
	if data is None:  # Reset message
		HTMXTemplate(
			template_name="components/message.html.jinja",
			context={"user": UserMessage(name="", email="", message="")},
		)
	return HTMXTemplate(
		template_name="components/message.html.jinja",
		context={"user": data},
	)


app = Litestar(
	route_handlers=[index, post_users_messages],
	debug=True,
	request_class=HTMXRequest,
	template_config=TemplateConfig(
		directory=Path("src/templates"),
		engine=JinjaTemplateEngine,
	),
	exception_handlers={
		NotFoundException: not_found_exception_handler,
		HTTPException: http_exception_handler,
		ValidationException: validation_exception_handler,
	},
	logging_config=logging_config,
)
