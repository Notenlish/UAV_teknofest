from __future__ import print_function

import os
import pygame
import pkg_resources
import yaml
import fnmatch

from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.lib import mp_util
from MAVProxy.modules.lib import mp_settings

import threading
import sys

# go from mavproxy folder to
start = sys.path[0]  # C:\\Users\\ihsan\\npmbugsolve\\UAV_teknofest\\MAVProxy\\MAVProxy
root = os.path.join(start, "..", "..")
sys.path.append(root)
# module load customui


# from MAVProxy.modules.mavproxy_customui import controls


class CustomUI(mp_module.MPModule):
    """
    customui set verbose
    customui set debug
    customui status
    customui probe
    """

    def __init__(self, mpstate):
        """Initialise module"""
        super(CustomUI, self).__init__(
            mpstate, "customui", "A flexible customui driver"
        )

        self.joystick = None

        self.init_pygame()
        self.init_settings()
        self.init_commands()

        self.probe()

    def log(self, msg, level=0):
        if self.mpstate.settings.moddebug < level:
            return

        print("{}: {}".format(__name__, msg))

    def init_pygame(self):
        self.log("Initializing pygame", 2)
        pygame.init()
        pygame.joystick.init()

        self.log("KAFAYI YICEM")

        def runapp(self):
            from app import App

            a = App(self.mpstate)
            a.run()

        self.app_thread = threading.Thread(target=runapp, args=(self,))
        self.app_thread.start()

    def init_settings(self):
        pass

    def init_commands(self):
        self.log("Initializing commands", 2)
        self.add_command(
            "customui",
            self.cmd_customui,
            "A flexible customui drvier",
            ["status", "probe"],
        )

    def load_definitions(self):
        self.log("Loading customui definitions", 1)

        self.joydefs = []
        search = []

        userjoysticks = os.environ.get(
            "MAVPROXY_JOYSTICK_DIR", mp_util.dot_mavproxy("joysticks")
        )
        if userjoysticks is not None and os.path.isdir(userjoysticks):
            search.append(userjoysticks)

        search.append(pkg_resources.resource_filename(__name__, "joysticks"))

        for path in search:
            self.log("Looking for joystick definitions in {}".format(path), 2)
            path = os.path.expanduser(path)
            for dirpath, dirnames, filenames in os.walk(path):
                for joyfile in filenames:
                    root, ext = os.path.splitext(joyfile)
                    if ext[1:] not in ["yml", "yaml", "json"]:
                        continue

                    joypath = os.path.join(dirpath, joyfile)
                    self.log("Loading definition from {}".format(joypath), 2)
                    with open(joypath, "r") as fd:
                        joydef = yaml.safe_load(fd)
                        joydef["path"] = joypath
                        self.joydefs.append(joydef)

    def probe(self):
        print("probe")

    def usage(self):
        """show help on command line options"""
        return "Usage: customui <status|set>"

    def cmd_customui(self, args):
        if not len(args):
            self.log("No subcommand specified.")
        elif args[0] == "status":
            self.cmd_status()
        elif args[0] == "probe":
            self.cmd_probe()
        elif args[0] == "help":
            self.cmd_help()

    def cmd_help(self):
        print("customui probe -- reload and match customui definitions")
        print("customui status -- show currently loaded definition, if any")

    def cmd_probe(self):
        self.log("Re-detecting available joysticks", 0)
        self.probe()

    def cmd_status(self):
        if self.joystick is None:
            print("No active joystick")
        else:
            print("Active joystick:")
            print("Path: {path}".format(**self.joystick.controls))
            print("Description: {description}".format(**self.joystick.controls))

    def idle_task(self):
        if self.joystick is None:
            return

        for e in pygame.event.get():
            override = self.module("rc").override[:]
            values = self.joystick.read()
            override = values + override[len(values) :]

            # self.log('channels: {}'.format(override), level=3)

            if override != self.module("rc").override:
                self.module("rc").override = override
                self.module("rc").override_period.force()


def init(mpstate):
    """initialise module"""
    return CustomUI(mpstate)
