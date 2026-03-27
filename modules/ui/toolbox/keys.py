import arcade


def apply_key(text: str, keycode: int, modifiers: int = 0, int_only=False) -> str:
    if keycode == arcade.key.BACKSPACE:
        return text[:-1]

    if keycode < 32 or keycode > 126:
        return text

    char = chr(keycode)

    if char.isalpha():
        shift = modifiers & arcade.key.MOD_SHIFT
        caps = modifiers & arcade.key.MOD_CAPSLOCK

        if bool(shift) ^ bool(caps):
            char = char.upper()
        else:
            char = char.lower()

    elif modifiers & arcade.key.MOD_SHIFT:
        shift_map = {
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "0": "0",
            "-": "_",
            "=": "+",
            "[": "{",
            "]": "}",
            "\\": "|",
            ";": ":",
            "'": '"',
            ",": "<",
            ".": ">",
            "/": "?",
            "`": "~",
        }
        char = shift_map.get(char, char)

    if int_only:
        try:
            return str(int(text + char))
        except Exception:
            return str(text)

    return text + char


def visual_key(key_code):

    key_name = "UNKNOWN"
    for name in dir(arcade.key):
        if getattr(arcade.key, name) == key_code:
            key_name = name
            break

    return key_name
