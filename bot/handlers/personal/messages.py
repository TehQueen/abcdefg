from aiogram import Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from typing import Any


router = Router(name=__name__) 

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject) -> Any:
    await message.answer(_("Hello, {name}!").format(
        name=message.from_user.full_name
    ))
