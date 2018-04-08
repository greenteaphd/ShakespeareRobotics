# Andy Han, Joweina Hsiao, and Nikhil Smith
# COMP 380 - Robotics Project
# April 8th, 2019

# This and the RobotServer only establishes connection if both are in the Robot and started
# using separate terminals. You cannot run LaptopClient on the laptop and RobotServer
# on the robot and get the same result.
# But good progress.
# Ask Susan how to tackle this issue.

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.1", 7000))
data = "Go to thee nunnery"
data = data.encode()
s.sendall(data)
print("SUCCESS!")
s.close()

