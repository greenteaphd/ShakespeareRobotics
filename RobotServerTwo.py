# Andy Han, Joweina Hsiao, and Nikhil Smith
# COMP 380 - Robotics Project
# April 15th, 2018
# Sets up the second server for the robot and allows the robot to know which line to say back.

import socket
import ev3dev.ev3 as ev3
import string

CHARACTERS_FULL = ["Nikhil", "Joweina", "Andy"]

CHARACTERS_SHORT = ["Nick", "Jo", "Andy"]

OTHER_BAD_WORDS = ["Enter", "Scene"]

FILE_NAME = "WorkProblems.txt"

###
# PLEASE DOUBLE CHECK THis INPUT PARAMETER BEFORE RUNNING THE PROGRAM.
###
CURRENT_CHARACTER = "Nick"


def removePunctuation(words):
    newWords = []
    for word in words:
        resultString = ""
        for char in word:
            if char not in string.punctuation:
                resultString += char
        newWords.append(resultString)
    return newWords

def indexAllLines(fileName):
    """ indexAllLines is a helper function to respond(). It creates two lists: allLines and firstWords, which contains a list
    representation of either an entire line of the play, or simply the first word in a given line. These indexes do not
    match up with the ones in Hamlet.txt because it skips over blank lines. """
    file = open(fileName, "r")
    allLines = []
    firstWords = []
    for currentLine in file:
        words = currentLine.split()
        if len(words) > 0:
            firstWord = words[0]
            firstWords.append(firstWord)
            words = removePunctuation(words)
            allLines.append(words)
    file.close()
    return allLines, firstWords


def maxAndMinLines(fileName):
    file = open(fileName, "r")
    lengths = []
    for currentLine in file:
        if len(currentLine) > 1:
            length = len(currentLine)
            lengths.append(length)
    maxLength = max(lengths)
    minLength = min(lengths)
    file.close()
    return maxLength, minLength


def respond(currentCharacter, previousLine, charactersShort):
    """ respond() is the main part of the algorithm for the robot's response.
    It returns a string with the lines following a part of a given previous line """
    allLines, firstWords = indexAllLines(FILE_NAME)
    respondString = ""
    charactersShort.remove(currentCharacter)
    for index1 in range(0, len(allLines)-1):
        currentLine = allLines[index1]
        currentLine = ' '.join(currentLine)
        if previousLine.lower() in currentLine.lower():
            prevLineNumber = index1
            for index2 in range(prevLineNumber + 1, len(allLines)):
                if (firstWords[index2] not in charactersShort) and (firstWords[index2] not in OTHER_BAD_WORDS):
                    responseLine = allLines[index2]
                    responseLine = ' '.join(responseLine)
                    respondString = respondString + responseLine + "\n"
                elif firstWords[index2] in charactersShort:
                    break
    return respondString


def processHumanSpeech(speech, maxLength, minLength):
    processedSpeech = speech
    if len(speech) >= maxLength/2:
        processedSpeech = speech[-minLength:]
    if speech[-1:] == " ":
        processedSpeech = speech[0:len(speech) - 1]
    return processedSpeech


def postProcessHumanSpeech(speech):
    postProcessed = ""
    for char in speech:
        if char not in string.punctuation:
            postProcessed += char
    return postProcessed


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
