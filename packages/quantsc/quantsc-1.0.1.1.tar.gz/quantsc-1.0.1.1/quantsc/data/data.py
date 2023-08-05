from datetime import datetime, timedelta

# When importing a submodule in the same folder, use this to help
# python know we are importing a submodule instead of a file. Since
# the default behavior looks for __random.py
# import __random as __random
import quantsc.data.__random as __random

def __get_date():
    # np.__random.__random
    pass

def generate_random(range,generate_type = "seasonal"):
    print("Go Home!")

    return

    today_str = datetime.today().strftime("%Y-%m-%d")
    start_str = (datetime.today() - timedelta(days=6)).strftime("%Y-%m-%d")
    if generate_type =="seasonal":
        ts = random.seasonal()
        return ts


if __name__ == "__main__":
    print(__random.seasonal())
