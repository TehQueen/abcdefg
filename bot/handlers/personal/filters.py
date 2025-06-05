from aiogram.types import Message
from aiogram.filters import Filter
from aiogram.utils.i18n import I18n


class I18nFilter(Filter):
    def __init__(self, key: str) -> None:
        self.key = key

    async def __call__(self, message: Message, i18n: I18n) -> bool:
        return message.text == i18n.gettext(self.key)
