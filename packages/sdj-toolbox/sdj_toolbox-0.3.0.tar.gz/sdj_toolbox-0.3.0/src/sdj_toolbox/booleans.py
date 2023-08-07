def is_int(string: str) -> bool:
    """
    Returns True if string can be converted in interger.
    Usage:
        is_int(str)
    """
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_float(string: str) -> bool:
    """
    Returns True if string can be converted in float.
    Usage:
        is_float(str)
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_numeric(string: str) -> bool:
    """
    Returns True if string is a numerical expression.
    Usage:
        is_numeric(str)
    """
    return is_float(string)


if __name__ == "__main__":
    print("Some tests...")

    print()

    int_tests = ["hello", "1", "1.25", "1,25", "1.", ".45","0.0.0"]
    print('is_int() Tests...')
    for test in int_tests:
        print(f"Test value: {test} -> {is_int(test)}")

    print()

    print('is_float() Tests...')
    for test in int_tests:
        print(f"Test value: {test} -> {is_float(test)}")

    print()

    print('is_numeric() Tests...')
    for test in int_tests:
        print(f"Test value: {test} -> {is_numeric(test)}")
