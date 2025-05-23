from time import monotonic

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.i18n.lazy_proxy import LazyProxy
from aiogram.utils.i18n import I18n

from typing import Callable, TypeAlias, Union, Protocol, runtime_checkable


KeyboardType: TypeAlias = Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]
ContextType: TypeAlias = Callable[..., LazyProxy]


@runtime_checkable
class KeyboardFactory(Protocol):
    def __call__(
            self,
            gettext: ContextType
        ) -> KeyboardType: ...


class LazyKeyboard:
    """
    Lazy initialization and caching of translated keyboards.

    Attributes:
        _struct: Keyboard factory
        _cache_expire: Cache lifetime
        _cached_locale: Keyboard cache by locale
        _last_updated: Last update time by locale
    """
    __slots__ = (
        "_struct",
        "_cache_expire",
        "_cached_locale",
        "_last_updated",
    )

    def __init__(
            self,
            struct: KeyboardFactory,
            cache_expire: float | None = None
        ) -> None:
        """
        Create a keyboard instance for lazy translation

        :struct (KeyboardFactory): Function for creating a keyboard
        :cache_expire (float | None): Cache lifetime in seconds (None - forever)
        """
        self._struct = struct
        self._cache_expire = cache_expire

        self._cached_locale: dict[str, KeyboardType] = {}
        self._last_updated: dict[str, float] = {}

    def __call__(
            self,
            i18n: I18n
        ) -> KeyboardType:
        """
        Returns the keyboard for the current locale, taking caching into account.

        Arguments:
            i18n (I18n): Internationalization object

        Returns:
            KeyboardType: Ready-made keyboard
        """
        (locale := i18n.current_locale) in i18n.locales \
            and locale or (locale := i18n.default_locale)
        now = monotonic()

        if locale not in self._cached_locale or self._is_cache_expired(locale, now):
            self._update_cache(locale, now, i18n.gettext)

        return self._cached_locale[locale]
    
    def _is_cache_expired(self, locale: str, current_time: float) -> bool:
        """Checks if the cache for a locale has expired."""
        if not self._cache_expire:
            return False
        
        last_updated = self._last_updated.get(locale, 0.0)
        return (current_time - last_updated) >= self._cache_expire
    
    def _update_cache(
            self,
            locale: str,
            current_time: float,
            gettext: ContextType
        ) -> None:
        """Updates the cache for the specified locale."""
        self._cached_locale[locale] = self._struct(gettext)

        if not self._cache_expire:
            self._last_updated[locale] = current_time
