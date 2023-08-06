def is_icao(code):
    """
    Check if the code is a valid ICAO code.
    """
    if len(code) != 4:
        return False
    if not code.isalpha():
        return False
    return True


def lower_icao(code):
    """
    Lower the ICAO code.
    """
    return code.lower()