def is_positive(number: int | float) -> bool:
    """
    Returns if given number is positive or not.
    (0 is considered as being positive.)

    :param number: Target number.
    """
    if number >= 0: return True
    else: return False