import configparser
import os
import base64
import logging
from typing import Text


class Params:
    def __init__(self, parameter_file="params.ini") -> None:
        self.logger = logging.getLogger("__main__.parameters")
        self.config_file = os.path.join("covid_analysis", "config", parameter_file)
        self.logger.info(
            f"Parameters are being initialized from config {self.config_file}"
        )
        self.read_config(self.config_file)

    def read_config(self, config_file) -> None:
        if os.path.exists(config_file):
            self.config = configparser.ConfigParser()
            self.config.read(config_file)
            self.host = self.config["mysql"]["host"]
            self.user = self.config["mysql"]["user"]
            self.passwd = self.decode_string(self.config["mysql"]["passwd"])
            self.db = self.config["mysql"]["db"]
            self.key = self.decode_string(self.config["api"]["key"])
            self.states_url = self.config["api"]["states_url"] + self.key
            self.states_url_timeseries = self.config["api"]["states_url_timeseries"] + self.key
            self.counties_url = self.config["api"]["counties_url"] + self.key
        else:
            raise Exception(f"{config_file} is not present at the location or invalid")

    @staticmethod
    def decode_string(message) -> Text:
        base64_message = message
        base64_bytes = base64_message.encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode("ascii")
        return message

    def encode_string(self, message) -> Text:
        message_bytes = message.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("ascii")
        return base64_message


if __name__ == "__main__":
    # Usage of the class
    param = Params()
    print(param.user)
