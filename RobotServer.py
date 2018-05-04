# Andy Han, Joweina Hsiao, and Nikhil Smith
# COMP 380 - Robotics Project
# May 5th, 2018
# Sets up the server for the robot and allows the robot to know which line to say back.
# This program is specific to the Hamlet play.

import socket
import ev3dev.ev3 as ev3
import string


###
# Static variables needed for respond() function
#   CHARACTERS_FULL is a list of all of the characters in Hamlet and their full names as listed in the Dramatis Personae
#   CHARACTERS_SHORT is a list of all of the characters in Hamlet and their shortened names as seen in the play's script
#   OTHER_BAD_WORDS is a list of words to ignore when creating a response
#   FILE is the read-only representation of Hamlet.txt
###

CHARACTERS_FULL = ["Claudius", "Hamlet", "Polonius", "Horatio", "Laertes", "Voltemand", "Cornelius", "Rosencrantz",
                  "Guildenstern","Osric","Gentleman","Priest","Marcellus","Bernardo","Francisco","Reynaldo",
                  "Players", "Two Clowns", "Fortinbras", "Norwegian Captain", "English Ambassador", "Gertrude",
                  "Ophelia","Ghost of Hamlet's Father","Lord","Lady","Officer","Solider","Sailor","Messenger","Attendant"]

CHARACTERS_SHORT = ["King", "Ham.", "Pol.", "Hor.", "Laer.", "Volt.", "Cor.", "Ros.", "Guil.", "Osr.", "Gent.", "Priest.",
                   "Mar.","Ber.","Fran.","Rey.","1. Play.", "Clown.", "Fort.","Capt.","Ambassador.","Queen.","Oph.",
                   "Ghost.","Lord.","","","","Sailor.","Mess.","Servant."]

OTHER_BAD_WORDS = ["Enter", "Scene", "Exeunt", "Flourish", "Exit"]

FILE_NAME = "Hamlet.txt"


###
# PLEASE DOUBLE CHECK THIS INPUT PARAMETER BEFORE RUNNING THE PROGRAM.
###
CURRENT_CHARACTER = "Ber."


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

    for i in range(2):
        print("The server is up and running!")
        conn, address = s.accept()
        data = conn.recv(1024)
        data = data.decode()
        test_method(data)
        conn.close()

server_main("169.254.55.85")  # Note that the IP of the robot will change each time a connection is made via Bluetooth

