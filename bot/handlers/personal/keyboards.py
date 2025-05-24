"""
Module: personal.keyboards
Description: Contains lazy-initialized inline keyboards for personal (1:1) bot interactions.
All keyboards are cached for 24 hours (86400 seconds) to optimize resource usage.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.utils.keyboards import LazyKeyboard


# Creates inline keyboard for the start command with localization support
cmd_start_kb = LazyKeyboard(
    lambda gettext: InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=gettext('⚙️'), callback_data="@settings"),
            InlineKeyboardButton(text=gettext('📢'), callback_data="@audience"),
        ],
        [InlineKeyboardButton(text=gettext('📈'), callback_data="@analytics")]
    ]), cache_expire=86400
)
