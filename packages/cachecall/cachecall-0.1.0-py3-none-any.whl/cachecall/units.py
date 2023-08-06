from typing import Union


def kb(val: Union[float, int]) -> Union[float, int]:
    return val * 1024


def mb(val: Union[float, int]) -> Union[float, int]:
    return val * 1024**2


def gb(val: Union[float, int]) -> Union[float, int]:
    return val * 1024**3
