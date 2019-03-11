import yaml
import os
import os.path
import sys
from decouple import config
token=config("TOKEN",default="xxxxxxxxxxxxxxxx")
def load_config(config_name):
    config_path="./configs/{}.yml".format(config_name)
    with open(config_path, 'r') as stream:
        try:
            CONFIG = yaml.load(stream)
        except Exception as e:
            print("There appears to be a syntax problem with your config.yml")
            raise e

        #[section, type, error message]
        sections = [
                    ["url", str, "Section `url` must be a string wrapped in quotes."],
                    ["good_luck_messages", list, "Chat messages on beginning of game."],
                    ["good_game_message", str, "Chat message on finishing game."],
                    ["engine", dict, "Section `engine` must be a dictionary with indented keys followed by colons.."],
                    ["challenge", dict, "Section `challenge` must be a dictionary with indented keys followed by colons.."],
                    ["max_concurrent_games", int, "Section `max_concurrent_games` must be an integer number without quotes."]]
        for section in sections:
            if section[0] not in CONFIG:
                raise Exception("Your config.yml does not have required section `{}`.".format(section[0]))
            elif not isinstance(CONFIG[section[0]], section[1]):
                raise Exception(section[2])

        engine_sections = [["dir", str, "´dir´ must be a string wrapped in quotes."],
                           ["name", str, "´name´ must be a string wrapped in quotes."]]

        for subsection in engine_sections:
            if subsection[0] not in CONFIG["engine"]:
                raise Exception("Your config.yml does not have required `engine` subsection `{}`.".format(subsection))
            if not isinstance(CONFIG["engine"][subsection[0]], subsection[1]):
                raise Exception("´engine´ subsection {}".format(subsection[2]))

        if token == "xxxxxxxxxxxxxxxx":
            raise Exception("Your config.yml has the default Lichess API token. This is probably wrong.")

        if not os.path.isdir(CONFIG["engine"]["dir"]):
            raise Exception("Your engine directory `{}` is not a directory.")

        engine = os.path.join(CONFIG["engine"]["dir"], CONFIG["engine"]["name"])

        if not os.path.isfile(engine):
            raise Exception("The engine %s file does not exist." % engine)

        if not os.access(engine, os.X_OK):
            raise Exception("The engine %s doesn't have execute (x) permission. Try: chmod +x %s" % (engine, engine))

        if "polyglot" in CONFIG["engine"] and CONFIG["engine"]["polyglot"]["enabled"] is True:
            book_paths=[]
            for book_name in CONFIG["engine"]["polyglot"]["books"]:
                book_dir = os.path.join(CONFIG["engine"]["dir"], book_name)
                if not os.path.isfile(book_dir):
                    raise Exception("The polyglot book %s file does not exist." % book_dir)
                book_paths.append(book_dir)

            CONFIG["engine"]["polyglot"]["books"] = book_paths

    return CONFIG
