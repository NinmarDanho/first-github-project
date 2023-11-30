def storlek_validera(storlek):
    """Denna funktion kontrollerar att inmatningen på brädets storlek är giltig."""
    if storlek.isnumeric():
        if int(storlek) >= 4:
            return True
        else:
            return False
    else:
        return False

def kontrollera_inmatning_trollposition(troll_position, rad_length):
    """Denna funktion kontrollerar att inmatningen på trollpositionen är korrekt."""
    if troll_position == "undo":
        return True
    elif troll_position.isnumeric():
        if int(troll_position) > 0 and int(troll_position) <= rad_length:
            return True
        else:
            return False
    else:
        return False

def fil_kontrollering():
    """Denna funktion kontrollerar om filen finns eller ej"""
    filnamn = 'Highscore.txt'
    try:
        studentfil = open(filnamn, 'r')
        return True
    except FileNotFoundError:
        return False

def validera_namn_inmatning(namn_inmatning):
    """Denna funktion ser spelaren får skriva sitt namn eller nick_namn i namnfältet"""
    if namn_inmatning == "":
        return False
    else:
        return True
