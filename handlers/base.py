from aiogram import Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message

from typing import Any


router = Router(name=__name__) 

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject) -> Any:
    await message.answer("Hello, World!")
