import arcade


def apply_key(text: str, keycode: int, modifiers: int = 0, int_only=False) -> str:
    """
    Applique la saisie d'une touche à une chaîne de caractères existante en tenant compte 
    des modificateurs (Majuscule, Verr. Maj) et des contraintes de type.
    """
    
    # Gérer la touche retour arrière pour supprimer le dernier caractère
    if keycode == arcade.key.BACKSPACE:
        return text[:-1]

    # Ignorer les touches de contrôle non imprimables (hors plage ASCII standard)
    if keycode < 32 or keycode > 126:
        return text

    char = chr(keycode)

    # Gérer la casse pour les caractères alphabétiques
    if char.isalpha():
        shift = modifiers & arcade.key.MOD_SHIFT
        caps = modifiers & arcade.key.MOD_CAPSLOCK

        # Appliquer la logique XOR pour déterminer si le caractère doit être en majuscule
        if bool(shift) ^ bool(caps):
            char = char.upper()
        else:
            char = char.lower()

    # Mapper les caractères spéciaux lorsque la touche Maj (Shift) est enfoncée
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

    # Si le mode 'entier uniquement' est activé, valider que la nouvelle chaîne est numérique
    if int_only:
        try:
            return str(int(text + char))
        except Exception:
            # En cas d'erreur de conversion, renvoyer le texte original sans modification
            return str(text)

    return text + char


def visual_key(key_code):
    """
    Récupère le nom symbolique d'une touche à partir de son code numérique
    en parcourant les attributs du module arcade.key.
    """
    key_name = "UNKNOWN"
    
    # Parcourir les constantes disponibles dans arcade.key pour trouver la correspondance
    for name in dir(arcade.key):
        if getattr(arcade.key, name) == key_code:
            key_name = name
            break

    return key_name