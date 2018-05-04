# Andy Han, Joweina Hsiao, and Nikhil Smith
# COMP 380 - Robotics Project
# May 3rd, 2018
# Sets up the second server for the robot and allows the robot to know which line to say back.
# This program is specific to the Troubles at Work play (WorkProblems.txt).

import socket
import ev3dev.ev3 as ev3
import string

###
# Static variables needed for respond() function
#   CHARACTERS_FULL is a list of all of the characters in the Troubles at Work play
#   CHARACTERS_SHORT is a list of all of the characters in Troubles at Work play and their shortened names
#   OTHER_BAD_WORDS is a list of words to ignore when creating a response
#   FILE is the read-only representation of WorkProblems.txt
###

CHARACTERS_FULL = ["Nikhil", "Joweina", "Andy"]

CHARACTERS_SHORT = ["Nick", "Jo", "Andy"]

OTHER_BAD_WORDS = ["Enter", "Scene"]

FILE_NAME = "WorkProblems.txt"

###
# PLEASE DOUBLE CHECK THIS INPUT PARAMETER BEFORE RUNNING THE PROGRAM.
###
CURRENT_CHARACTER = "Jo"

###
# Methods used to generate the correct response to a given line in the play
###

def removePunctuation(inputString):
    """ Removes punctuation from a string """
    newString = inputString
    for char in inputString:
        if char not in string.punctuation:
            newString += char
    return newString

def indexLines(fileName):
    """ indexAllLines is a helper function to respond(). It creates two lists: allLines and firstWords, which contains a list
    representation of either an entire line of the play, or simply the first word in a given line. These indexes do not
    match up with the ones in Hamlet.txt because it skips over blank lines. """
    file = open(fileName, "r")
    lengths = []
    allLines = []
    firstWords = []
    for currentLine in file:
        if len(currentLine) > 1:
            length = len(currentLine)
            lengths.append(length)
        words = currentLine.split()
        if len(words) > 0:
            firstWord = words[0]
            firstWords.append(firstWord)
            allLines.append(words)
    file.close()
    return allLines, firstWords

def respond(currentCharacter, previousLine, charactersShort):
    """ respond() is the main part of the algorithm for the robot's response.
    It returns a string with the lines following a part of a given previous line """
    allLines, firstWords = indexLines(FILE_NAME)
    respondString = ""
    charactersShort.remove(currentCharacter)
    for index1 in range(0, len(allLines)-1):
        currentLine = allLines[index1]
        currentLine = ' '.join(currentLine)
        currentLine = removePunctuation(currentLine)
        if previousLine.lower() in currentLine.lower():
            prevLineNumber = index1
            for index2 in range(prevLineNumber + 1, len(allLines)-1):
                if firstWords[index2] not in charactersShort and firstWords[index2] not in OTHER_BAD_WORDS:
                    responseLine = allLines[index2]
                    responseLine = ' '.join(responseLine)
                    respondString = respondString + responseLine + "\n"
                elif firstWords[index2] in charactersShort:
                    break
    respondString = respondString[2:]
    charactersShort.append(currentCharacter)
    return respondString

def test_method(string_input):
    """ Tests the server_main method to see if the data was sent correctly. """
    response_string = respond(CURRENT_CHARACTER, string_input, CHARACTERS_SHORT)
    print(response_string)

    print("The client sent: " + string_input)
    ev3.Sound.set_volume(100)
    ev3.Sound.speak(response_string, espeak_opts= '-a 200 -s 130 -v "hi" -g 7 -k 20')
    print(response_string)

def server_main(server_address):
    """ This method receives the message sent by the client. """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server_address, 7000))
    s.listen(10)

    for i in range(10):
        print("The server is up and running!")
        conn, address = s.accept()
        data = conn.recv(1024)
        data = data.decode()
        test_method(data)
        conn.close()

server_main("169.254.151.186")  # Note that the IP of the robot will change each time a connection is made via Bluetooth