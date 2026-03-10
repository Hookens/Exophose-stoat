from typing import Type, TypeVar, TYPE_CHECKING, cast

if TYPE_CHECKING:
    from stoat.ext.commands import Bot, Gear

T = TypeVar("T")


def get_gear(bot: "Bot", gear: str):
    """
    Retrieve a gear by its class with proper typing.
    Raises ValueError if the gear is missing.
    """

    gear = bot.get_gear(gear)
    if gear is None:
        raise ValueError(f"Gear '{gear}' is not loaded.")

    return gear
