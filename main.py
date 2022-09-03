from auto_clicker import AutoClicker
from logo import logo


def validate_input(user_input: str) -> int:
    try:
        valid_input = int(user_input)
    except ValueError:
        valid_input = validate_input(user_input=input("Please input an integer: "))
    finally:
        return valid_input


print(logo)
print("Welcome to CookieClicker+")
cookie_clicker = AutoClicker()
stop_after_min = validate_input(user_input=input("How long would you like to auto-click for? (min) "))
break_after_sec = validate_input(user_input=input("How often would you like to buy upgrade? (sec) "))
cookie_clicker.auto_click(stop_after_min=stop_after_min, break_after_sec=break_after_sec)
