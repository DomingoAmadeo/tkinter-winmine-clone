from configparser import ConfigParser


def create_ini():
    config_parser.add_section("settings")
    config_parser.set("settings", "difficulty", "0")
    config_parser.set("settings", "marks", "0")
    config_parser.add_section("current")
    config_parser.set("current", "columns", "9")
    config_parser.set("current", "rows", "9")
    config_parser.set("current", "mines", "10")
    config_parser.add_section("records")
    config_parser.set("records", "beginner", "999,Anonymus")
    config_parser.set("records", "intermediate", "999,Anonymus")
    config_parser.set("records", "expert", "999,Anonymus")
    config_parser.set("records", "nightmare", "999,Anonymus")
    with open("minesweeper_config.ini", "w") as output:
        config_parser.write(output)

def update (section, key, value):
    config_parser.set(section, key, value)
    with open("minesweeper_config.ini", "w") as output:
        config_parser.write(output)

def get_difficulty(difficulty : int):
    default_difficulties = [
    {"name" : "Beginner",
     "columns" : "9",
     "rows" : "9",
     "mines" : "10"},
    {"name" : "Intermediate",
     "columns" : "16",
     "rows" : "16",
     "mines" : "40"},
    {"name" : "Expert",
     "columns" : "30",
     "rows" : "16",
     "mines" : "99"},
    {"name" : "Nightmare",
     "columns" : "30",
     "rows" : "30",
     "mines" : "225"}]

    if difficulty in range(4):
        new_difficulty = default_difficulties[difficulty]
    elif difficulty == 4:
        new_difficulty = {"name" : "Custom", **dict(config_parser.items("current"))}
    else:
        new_difficulty = default_difficulties[0]
        
    update("settings", "difficulty", str(difficulty))
    for key, value in new_difficulty.items():
        if not key == "name":
            update("current", key, value)

def value_get(section, key):
    return config_parser.getint(section, key)

def records_get():
    return dict(config_parser.items("records"))

def size_get(size, f):
    return size + (f() * 16)

config_parser = ConfigParser()

if config_parser.read("minesweeper_config.ini") == []:
    create_ini()
config_parser.read("minesweeper_config.ini")

COLUMNS = lambda: value_get("current", "columns")
ROWS = lambda: value_get("current", "rows")
MINES = lambda: value_get("current", "mines")
DIFFUCULTY = lambda: value_get("settings", "difficulty")
RECORDS = lambda: records_get()
WIDTH = lambda: size_get(20, COLUMNS)
HEIGHT = lambda: size_get(62, ROWS)


