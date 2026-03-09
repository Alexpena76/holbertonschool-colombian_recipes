def repeating():
    """Returns the first character which isn't repeating in a string, or None if there is no such character-"""
    s = "String"
    for a in s:
        if s.count(a) == 1:
            return a
    return None