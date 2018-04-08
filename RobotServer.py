# Andy Han, Joweina Hsiao, and Nikhil Smith
# COMP 380 - Robotics Project
# Reference purpose. This file would be run on the robot.
# April 8th, 2019

import socket


def test_method(string_input):
    print("It worked! " + string_input)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.0.1", 7000))
s.listen(10)

while True:
    print("It's still running!")
    conn, addr = s.accept()
    data = conn.recv(1024)
    data = data.decode()
    test_method(data)
    print("it's still here")
    conn.close()

