import re


def is_valid_city_name(city_name):
    
    pattern = r"^[A-Za-zÀ-ÿ\s\-'.]{2,60}$"
    return bool(re.fullmatch(pattern, city_name.strip()))


def is_valid_menu_choice(choice, allowed_choices):
 
    return choice in allowed_choices