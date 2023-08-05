from honkaiDex import gconfig

def valid_na_uid(uid : str) -> bool:
    """
    Check if the uid is valid.
    """
    try:
        uid_str = str(uid)
        uid_int = int(uid)
    except:
        return False

    if not uid_str.isdigit():
        return False

    if len(uid_str) != 9:
        return False

    if uid_str[0] != "1":
        return False

    return True

def valid_lv(lv : str) -> bool:
    """
    Check if the lv is valid.
    """
    try:
        int_lv = int(lv)
    except:
        return False

    if lv is None or lv == "":
        return False
    
    minlv = gconfig.MIN_LV
    maxlv = gconfig.MAX_LV

    if minlv <= int_lv <= maxlv:
        return True
    return False

def calculate_stamina(lv : int, current :int):
    max_stamina = lv + 80
    if current > max_stamina:
        return 0
    return (max_stamina - current) * 6