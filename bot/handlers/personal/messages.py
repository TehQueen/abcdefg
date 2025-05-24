from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.i18n import I18n, gettext as _

from typing import Any

from bot.database.models import User
from bot.handlers.personal.keyboards import cmd_start_kb


router = Router(name=__name__) 

@router.message(CommandStart())
async def cmd_start(message: Message, user: User, i18n: I18n) -> Any:
    return await message.answer(_("cmd-start").format(
        name=user.full_name
    ), reply_markup=cmd_start_kb(i18n))

@router.message(Command("settings"))
async def cmd_settings(message: Message) -> Any:
    return await message.answer(_("cmd_settings"))

@router.message(Command("help"))
async def cmd_help(message: Message, i18n: I18n) -> Any:
    return await message.answer(_("cmd-help"), reply_markup=cmd_start_kb(i18n))
