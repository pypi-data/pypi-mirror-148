# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybotx',
 'pybotx.bot',
 'pybotx.bot.api',
 'pybotx.bot.api.responses',
 'pybotx.bot.middlewares',
 'pybotx.client',
 'pybotx.client.bots_api',
 'pybotx.client.chats_api',
 'pybotx.client.events_api',
 'pybotx.client.exceptions',
 'pybotx.client.files_api',
 'pybotx.client.notifications_api',
 'pybotx.client.smartapps_api',
 'pybotx.client.stickers_api',
 'pybotx.client.users_api',
 'pybotx.models',
 'pybotx.models.message',
 'pybotx.models.system_events']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0,<0.9.0',
 'httpx>=0.18.0,<0.22.0',
 'loguru>=0.6.0,<0.7.0',
 'mypy-extensions>=0.2.0,<0.5.0',
 'pydantic>=1.6.0,<1.9.0',
 'typing-extensions>=3.7.4,<5.0.0']

setup_kwargs = {
    'name': 'pybotx',
    'version': '0.39.0',
    'description': 'A python library for interacting with eXpress BotX API',
    'long_description': '# pybotx\n\n*Библиотека для создания чат-ботов и SmartApps для мессенджера eXpress*\n\n[![PyPI version](https://badge.fury.io/py/botx.svg)](https://badge.fury.io/py/pybotx)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybotx)\n[![Coverage](https://codecov.io/gh/ExpressApp/pybotx/branch/master/graph/badge.svg)](https://codecov.io/gh/ExpressApp/pybotx/branch/master)\n[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n\n## Особенности\n\n* Простая для использования\n* Поддерживает коллбэки BotX\n* Легко интегрируется с асинхронными веб-фреймворками\n* Полное покрытие тестами\n* Полное покрытие аннотациями типов\n\n\n## Установка\n\nИспользуя `pip`:\n\n```bash\npip install git+https://github.com/ExpressApp/pybotx.git\n```\n\n**Предупреждение:** Данный проект находится в активной разработке (`0.y.z`) и\nего API может быть изменён при повышении минорной версии.\n\n\n## Минимальный пример бота (интеграция с FastAPI)\n\n```python\nfrom http import HTTPStatus\nfrom uuid import UUID\n\nfrom fastapi import FastAPI, Request\nfrom fastapi.responses import JSONResponse\n\nfrom pybotx import (\n    Bot,\n    BotAccountWithSecret,\n    HandlerCollector,\n    IncomingMessage,\n    build_command_accepted_response,\n)\n\ncollector = HandlerCollector()\n\n\n@collector.command("/echo", description="Send back the received message body")\nasync def echo_handler(message: IncomingMessage, bot: Bot) -> None:\n    await bot.answer_message(message.body)\n\n\nbot = Bot(\n    collectors=[collector],\n    bot_accounts=[\n        BotAccountWithSecret(  # noqa: S106\n            # Не забудьте заменить эти учётные данные на настоящие\n            id=UUID("123e4567-e89b-12d3-a456-426655440000"),\n            host="cts.example.com",\n            secret_key="e29b417773f2feab9dac143ee3da20c5",\n        ),\n    ],\n)\n\napp = FastAPI()\napp.add_event_handler("startup", bot.startup)\napp.add_event_handler("shutdown", bot.shutdown)\n\n\n@app.post("/command")\nasync def command_handler(request: Request) -> JSONResponse:\n    bot.async_execute_raw_bot_command(await request.json())\n    return JSONResponse(\n        build_command_accepted_response(),\n        status_code=HTTPStatus.ACCEPTED,\n    )\n\n\n@app.get("/status")\nasync def status_handler(request: Request) -> JSONResponse:\n    status = await bot.raw_get_status(dict(request.query_params))\n    return JSONResponse(status)\n\n\n@app.post("/notification/callback")\nasync def callback_handler(request: Request) -> JSONResponse:\n    bot.set_raw_botx_method_result(await request.json())\n    return JSONResponse(\n        build_command_accepted_response(),\n        status_code=HTTPStatus.ACCEPTED,\n    )\n```\n',
    'author': 'Sidnev Nikolay',
    'author_email': 'nsidnev@ccsteam.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ExpressApp/pybotx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
