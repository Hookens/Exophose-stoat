from typing import Type, TypeVar, TYPE_CHECKING, cast

if TYPE_CHECKING:
    from stoat.ext.commands import Bot

T = TypeVar("T")


def get_gear(bot: 'Bot', gear_type: Type[T]) -> T:
    """
    Retrieve a gear by its class with proper typing.
    Raises ValueError if the gear is missing.
    """
    
    gear = bot.get_gear(gear_type.__name__)
    if gear is None:
        raise ValueError(f"Gear '{gear_type.__name__}' is not loaded.")

    return cast(T, gear)
