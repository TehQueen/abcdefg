from aiogram import Router
from aiogram.types import CallbackQuery

from typing import Any


router = Router(name=__name__)

@router.callback_query()
async def cb_start(callback: CallbackQuery) -> Any:
    match callback.data:
        case "@settings":
            return await callback.answer("Settings")
        case "@audience":
            return await callback.answer("Audience")
        case "@analytics":
            return await callback.answer("Analytics")
    return await callback.answer("Distribution error", show_alert=True)
