"""Rejex is a tool used to build regex expressions for python."""

from .rejex_class import Rejex
from .rejex_static import *

def test_regex(regex_pattern:str, string:str, flag:int=0) -> bool:
    matched = bool(match(regex_pattern, string, flag))
    print(f"-------------------------------\nregex_pattern='{regex_pattern}'\nstring='{string}'\nmatch={matched}\n-------------------------------")

class CommonRejex:
    phone_number: str = r"(\+(\d)+)? ?(\()?(\d){3}(\))? ?(\d){3}((-| ))?(\d){4}"
    """ 
    (
        Rejex()
            .zero_or_one(
                Rejex()
                    .literal("+")
                    .one_or_more(
                        Static.any_number()
                    )
                    .compile()
            )
            .zero_or_one(Static.literal(" "))
            .zero_or_one(Static.literal("("))
            .n_number_times(3, Static.any_number())
            .zero_or_one(Static.literal(")"))
            .zero_or_one(Static.literal(" "))
            .n_number_times(3, Static.any_number())
            .zero_or_one(Static.alternative(Static.literal("-"), Static.literal(" ")))
            .n_number_times(4, Static.any_number())
        .compile()
    )
    ...
    """

    short_date:str = r"(\d)?\d(/|-)(\d)?\d(/|-)((\d){2})?(\d){2}"
    """
    (
        Rejex()
            .zero_or_one(Static.any_number())
            .any_number()
            .alternative(Static.literal("/"), Static.literal("-"))
            .zero_or_one(Static.any_number())
            .any_number()
            .alternative(Static.literal("/"), Static.literal("-"))
            .zero_or_one(
                Static.n_number_times(2, Static.any_number())
            )
            .n_number_times(2, Static.any_number())
        .compile()
    )"""

    basic_time:str = r"[0-9]?[0-9]:[0-9][0-9](:[0-9][0-9])?"