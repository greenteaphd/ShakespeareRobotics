# Andy Han, Joweina Hsiao, and Nikhil Smith
# COMP 380 - Robotics Project
# April 8th, 2019

import socket

hamlet_soliloquy = "To be, or not to be--that is the question: Whether 'tis nobler in the mind to suffer. "


def client_main(server_address):
    """ This method takes in a server address in order to send data to the server. """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_address, 7000))
    data = hamlet_soliloquy
    data = data.encode()
    s.sendall(data)
    print("SUCCESS!")
    s.close()
    return

client_main("169.254.228.234")
