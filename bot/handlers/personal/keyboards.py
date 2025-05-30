"""
Module: personal.keyboards
Description: Contains lazy-initialized inline and reply keyboards for personal bot interactions.
All keyboards are cached for 24 hours (86400 seconds) to optimize resource usage.
"""

from aiogram.types import LoginUrl, WebAppInfo
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.core import settings
from bot.utils.keyboards import LazyKeyboard


# Creates inline keyboard for the start command with localization support
cmd_start_kb_rp = LazyKeyboard(
    lambda gettext: ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=gettext('📢')),
            KeyboardButton(text=gettext('🧙‍♂️')),
        ],
        [KeyboardButton(text=gettext('⚙️'), web_app=WebAppInfo(url=settings.WEBAPP_EP))],
    ], resize_keyboard=True, one_time_keyboard=True), cache_expire=86400
)

cmd_start_kb_il = LazyKeyboard(
    lambda gettext: InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=gettext('⚙️'), login_url=LoginUrl(url=settings.WEBAPP_EP)),
        ],
    ]), cache_expire=86400
)
