# Andy Han, Joweina Hsiao, and Nikhil Smith
# COMP 380 - Robotics Project
# April 8th, 2019

import socket
import ev3dev.ev3 as ev3


def test_method(string_input):
    """ Tests the server_main method to see if the data was sent correctly. """
    print("The client sent: " + string_input)
    ev3.Sound.set_volume(100)
    ev3.Sound.speak(string_input, espeak_opts= '-a 200 -s 130 -v "en-uk-wmids" -g 7 -k 20')


def server_main(server_address):
    """ This method receives the message sent by the client. """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server_address, 7000))
    s.listen(10)

    for i in range(1):
        print("The server is up and running!")
        conn, address = s.accept()
        data = conn.recv(1024)
        data = data.decode()
        test_method(data)
        conn.close()

server_main("169.254.228.234")

