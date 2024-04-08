import enum

from server.commands import COMMANDS, Command

class SCAN_RESULTS(enum.IntEnum):
    FOUND_SOLDIER = enum.auto()
    NOTHING = enum.auto() 



class UAV:
    def __init__(self) -> None:
        pass

    def move_to(self, coord):
        pass

    def search_area(self):
        # already arrived in area, now search
        result = self.scan_nearby()
        if result.type == SCAN_RESULTS.FOUND_SOLDIER:
            cmd = Command(COMMANDS.FOUND_SOLDIER, data={"gps_location":self.get_current_loc()})
            self.send_cmd(cmd)
            return
        elif result.type == SCAN_RESULTS.NOTHING:
            start_loc = self.get_current_loc()
            count = 0
            while True:
                self.move_forward(4 + count) # meters 
                result = self.scan_nearby()
                if result.type == SCAN_RESULTS.FOUND_SOLDIER:
                    cmd = Command(COMMANDS.FOUND_SOLDIER, data={"gps_location":self.get_current_loc()})
                    self.send_cmd(cmd)
                    break
                else:
                    if self.distance_to(start_loc) > 1_000: # 1km
                        cmd = Command(COMMANDS.CANT_FIND_SOLDIER, data={})
                        self.send_cmd(cmd)
                        break
                    self.rotate_deg(5)
                    count += 1