from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.i18n import I18n, gettext as _

from typing import Any

from bot.database.models import User
from bot.handlers.personal.keyboards import cmd_start_kb_il, cmd_start_kb_rp


router = Router(name=__name__) 

@router.message(CommandStart())
async def cmd_start(message: Message, user: User, i18n: I18n) -> Any:
    stk = "CAACAgIAAxkBAAIQXWg58j9hOdB1AYC9Juma7XvrgVRFAALsUwACgHSQS7FGQPxX0N6VNgQ"
    await message.answer_sticker(stk, reply_markup=cmd_start_kb_rp(i18n))
    return await message.answer(_("cmd-start").format(
        name=user.full_name
    ), reply_markup=cmd_start_kb_il(i18n))
