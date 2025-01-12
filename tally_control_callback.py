#!/usr/bin/env python

import logging
import sys
import time
import socket

from rtmidi.midiutil import open_midiinput

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)

tally_ip = "10.10.10.10"
tally_port = 5005
tcp_buffer = 1024
myip = "10.10.10.9"


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        if not self.message_filter(deltatime=deltatime, message=message):
            print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))

    def message_filter(self, deltatime, message):
        message_string = None
        if message == [144, 38, 127]:
            message_string = "LED1;Off;HostA;Mute;On"
        if message == [144, 38, 63]:
            message_string = "LED1;On;HostA;Mute;Off"
        if message == [144, 39, 127]:
            message_string = "LED2;Off;HostB;Mute;On"
        if message == [144, 39, 63]:
            message_string = "LED2;On;HostB;Mute;Off"
        if message == [144, 40, 127]:
            message_string = "LED3;Off;HostC;Mute;On"
        if message == [144, 40, 63]:
            message_string = "LED3;On;HostC;Mute;Off"
        if message == [144, 41, 127]:
            message_string = "LED4;Off;HostD;Mute;On"
        if message == [144, 41, 63]:
            message_string = "LED4;On;HostD;Mute;Off"
        if message == [144, 42, 127]:
            message_string = "LED5;Off;Brett;Mute;On"
        if message == [144, 42, 63]:
            message_string = "LED5;On;Brett;Mute;Off"

        if message_string is not None:
            print("[%s] @%0.6f %r [%s]" % (self.port, self._wallclock, message, message_string))
            send_tcp_packet(message_string)
            return True
        else:
            return False


def send_tcp_packet(message):
    # UDP
    sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_DGRAM) # UDP
    sock.sendto(message, (tally_ip, tally_port))
    # TCP
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind((myip, 0))
    # s.connect((tally_ip, tally_port))
    # s.send(message)
    # s.close()


def main():
    # Prompts user for MIDI input port, unless a valid port number or name
    # is given as the first argument on the command line.
    # API backend defaults to ALSA on Linux.
    port = sys.argv[1] if len(sys.argv) > 1 else None

    try:
        midiin, port_name = open_midiinput(port)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    print("Attaching MIDI input callback handler.")
    midiin.set_callback(MidiInputHandler(port_name))

    print("Entering main loop. Press Control-C to exit.")
    try:
        # Just wait for keyboard interrupt,
        # everything else is handled via the input callback.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midiin.close_port()
        del midiin


if __name__ == "__main__":
    main()
