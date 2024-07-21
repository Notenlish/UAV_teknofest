import enum
import json
from typing import Any, Type

import utils
from cryptography.fernet import Fernet


class MSG_SIZE_BIG(Exception):
    pass


class COMMANDS(enum.IntEnum):
    CONNECT = enum.auto()
    DISCONNECT = enum.auto()
    HEARTBEAT = enum.auto()  # nothing to send, used to pass msg sending to the server
    FOUND_SOLDIER = enum.auto()
    CANT_FIND_SOLDIER = enum.auto()
    SETUP = enum.auto()
    SETUP_RC = enum.auto()
    ARM_MOTORS = enum.auto()
    WAIT_ALT = enum.auto()
    TAKEOFF = enum.auto()
    HOVER = enum.auto()
    AUTO_CONTROL = enum.auto()
    GO_TO = enum.auto()
    LAND = enum.auto()
    DISARM_MOTORS = enum.auto()
    LISTENING = enum.auto()
    STOP = enum.auto()
    MOVE_TO = enum.auto()
    SOLDIER_SPOTTED = enum.auto()
    KAMIKAZE = enum.auto()
    TEST_RANGE_UBIQUITI = enum.auto()
    TEST_RANGE_TELEMETRY = enum.auto()


class Command:
    def __init__(self, type, data: dict[str, Any]) -> None:
        self.type: int = type
        self.data = data
        self._reset_tuples()

    def _reset_tuples(self):
        # fix assert not working because of json changing tuples to list
        for key, value in self.data.items():
            if type(value) == tuple:
                self.data[key] = list(value)

    @staticmethod
    def to_dict(cmd):
        _dict = {}
        _dict["TYPE"] = cmd.type
        _dict["DATA"] = cmd.data
        return _dict

    @classmethod
    def from_dict(cls, _dict: dict[str, Any]):
        return cls(_dict["TYPE"], _dict["DATA"])

    def __str__(self) -> str:
        return f"<Command {COMMANDS(self.type).name} {self.data} />"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        if self.type != other.type:
            return False
        if self.data != other.data:
            return False
        return True


class CommandConverter:
    def __init__(self) -> None:
        try:
            self.key = utils.read_config("../config.json")["ENCRYPT_KEY"]
        except FileNotFoundError:
            self.key = utils.read_config("config.json")["ENCRYPT_KEY"]
        self.encrypter = Fernet(self.key)

    def msg_from_command(self, command: Command):
        _str = json.dumps(Command.to_dict(command))
        _encrypted_str = self.encrypter.encrypt(_str.encode("utf8"))
        # print(f"size of encrypted_str is: {len(_encrypted_str)}")
        if len(_encrypted_str) > 1024:
            raise MSG_SIZE_BIG
        return _encrypted_str

    def command_from_msg(self, msg: bytes):
        _decrypted_str = self.encrypter.decrypt(msg).decode("utf8")
        _dict = json.loads(_decrypted_str)
        return Command.from_dict(_dict)


if __name__ == "__main__":
    command = Command(type=COMMANDS.GO_TO, data={"GPS_LOCATION": (33.5973, 73.0479)})
    command_converter = CommandConverter()
    msg = command_converter.msg_from_command(command)
    new_command = command_converter.command_from_msg(msg)
    print(command)
    print(new_command)
    assert command == new_command
