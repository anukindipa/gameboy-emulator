def d8_to_s8(value):
    """Convert an 8-bit unsigned integer to a signed integer."""
    if value >= 0x80:
        return value - 0x100
    return value