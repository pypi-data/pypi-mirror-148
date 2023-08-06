import json
from os.path import abspath, join


class Db(object):
    @classmethod
    def read_db_config(cls, file_name="config.json", choose_db="CN"):
        cls.base_dir = abspath(".")
        config_path = join(cls.base_dir, file_name)
        with open(config_path, "r", encoding="utf-8") as fp:
            cls.db_config = dict(json.load(fp)).get(choose_db)

    def __del__(self):
        self.conn.close_connect()
