import time
import rtmidi

accepted_names = ["MIDI Control 1"]


def midi_setup():
    midi_in = rtmidi.MidiIn()
    available_ports = midi_in.get_ports()
    desired_port = None
    for index, port in enumerate(available_ports):
        if port in accepted_names:
            desired_port = index
            break

    if desired_port is not None:
        midi_in.open_port(desired_port)

    if midi_in.is_port_open():
        print("Connected to: " + midi_in.get_port_name(desired_port))
        return midi_in
    else:
        print("Connection Failed: available midi ports are as follows")
        print(available_ports)
        return None

def midi_callback():
    pass

def main_loop(midi_in):
    while True:
        midi_data = midi_in.get_message()
        if midi_data is not None:
            print(midi_data)
        else:
            time.sleep(0.001)

def message_handler(midi_data):
    midi_message = midi_data[0]
    midi_delta = midi_data[1]
    

if __name__ == "__main__" :
    midi_in = midi_setup()
    if midi_in is not None:
        main_loop(midi_in=midi_in)


