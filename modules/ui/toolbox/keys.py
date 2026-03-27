import arcade


def apply_key(text: str, keycode: int, modifiers: int = 0, int_only=False) -> str:
    """
    Applique la saisie d'une touche à une chaîne de caractères existante, en gérant 
    les modificateurs comme Shift et Caps Lock.
    
    Args:
        text (str): Le texte actuel.
        keycode (int): Le code de la touche pressée.
        modifiers (int): Les modificateurs de clavier (Shift, etc.).
        int_only (bool): Si True, restreint la sortie à des valeurs entières uniquement.
        
    Returns:
        str: La chaîne de caractères mise à jour.
    """
    # Gérer la touche retour arrière (backspace)
    if keycode == arcade.key.BACKSPACE:
        return text[:-1]

    # Ignorer les touches non imprimables (en dehors de la plage ASCII standard)
    if keycode < 32 or keycode > 126:
        return text

    char = chr(keycode)

    # Gérer la casse pour les caractères alphabétiques
    if char.isalpha():
        shift = modifiers & arcade.key.MOD_SHIFT
        caps = modifiers & arcade.key.MOD_CAPSLOCK

        # Utilisation de l'opérateur XOR pour déterminer la casse finale
        if bool(shift) ^ bool(caps):
            char = char.upper()
        else:
            char = char.lower()

    # Appliquer la table de correspondance si la touche Shift est active pour les caractères spéciaux
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

    # Si seuls les entiers sont autorisés, valider la conversion
    if int_only:
        try:
            return str(int(text + char))
        except Exception:
            # En cas d'erreur de conversion, renvoyer le texte original
            return str(text)

    return text + char


def visual_key(key_code):
    """
    Identifie le nom textuel d'une touche à partir de son code numérique 
    en parcourant les constantes de la bibliothèque arcade.
    """
    key_name = "INCONNU"
    for name in dir(arcade.key):
        if getattr(arcade.key, name) == key_code:
            key_name = name
            break

    return key_name