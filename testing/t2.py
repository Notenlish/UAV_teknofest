import xpc


def ex():
    print("X-Plane Connect example script")
    print("Setting up simulation")
    with xpc.XPlaneConnect() as client:
        # Verify connection
        try:
            # If X-Plane does not respond to the request, a timeout error
            # will be raised.
            client.getDREF("sim/test/test_float")
        except:
            print("Error establishing connection to X-Plane.")
            print("Exiting...")
            return

        client.sendDREF("sim/flightmodel/position/P", 180)
        client.sendDREF("sim/flightmodel/position/Q", -180)

        # Let the sim run for a bit.

        # Make sure gear was stowed successfully
        # gear_status = client.getDREF(gear_dref)
        # if gear_status[0] == 0:
        #    print("Gear stowed")
        # else:
        #    print("Error stowing gear")

        print("End of Python client example")


if __name__ == "__main__":
    ex()
