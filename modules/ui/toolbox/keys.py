import arcade

def apply_key(text: str, keycode: int, modifiers: int = 0) -> str:
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
            "'": "\"",
            ",": "<",
            ".": ">",
            "/": "?",
            "`": "~",
        }
        char = shift_map.get(char, char)

    return text + char