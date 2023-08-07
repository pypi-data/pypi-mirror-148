from string import ascii_lowercase, ascii_uppercase


def rot_encode(text: str, rotation: int) -> str:
    """
    Returns text rotated version of text.
    Usage:
        rotated_txt = rot_encode("Hello World!", rotation=13)
    """
    base_chars = ascii_lowercase + ascii_uppercase
    rot_chars = ascii_lowercase[rotation:] + ascii_lowercase[:rotation] + ascii_uppercase[rotation:] + ascii_uppercase[:rotation]
    rot_dict = dict(zip(base_chars, rot_chars))
    return "".join([rot_dict[c] if c in rot_dict else c for c in text])


def rot_decode(text: str, rotation: int) -> str:
    """
    Returns text reversed rotation version of text.
    Usage:
        decoded_text = rot_decode("Tqxxa Iadxp!", rotation=12)
    """
    return rot_encode(text, -rotation)


def rot13(text: str) -> str:
    """
    Returns ROT13 version of text.
    Usage:
        rot13_txt = rot13("Hello World!")
    """
    return rot_encode(text, 13)


if __name__ == '__main__':
    text = "Hello World!"
    rot_text = rot13(text)
    unrot_text = rot_decode(rot_text, 13)

    print(f"Base string: {text}")
    print(f"ROT13 string: {rot_text}")
    print(f"UNROT13 string: {unrot_text}")

