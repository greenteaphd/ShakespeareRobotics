# Andy Han, Joweina Hsiao, and Nikhil Smith
# COMP 380 - Robotics Project
# April 15th, 2018
# This is just the program that deals with spitting back the correct lines after a line is spoken.
# Not related to the networking component.

###
# Static variables needed for respond() function
#   CHARACTERS_FULL is a list of all of the characters in Hamlet and their full names as listed in the Dramatis Personae
#   CHARACTERS_SHORT is a list of all of the characters in Hamlet and their shortened names as seen in the play's script
#   OTHER_BAD_WORDS is a list of words to ignore when creating a response
#   FILE is the read-only representation of Hamlet.txt
###

import string
import speech_recognition as sr

CHARACTERS_FULL = ["Claudius", "Hamlet", "Polonius", "Horatio", "Laertes", "Voltemand", "Cornelius", "Rosencrantz",
                  "Guildenstern","Osric","Gentleman","Priest","Marcellus","Bernardo","Francisco","Reynaldo",
                  "Players", "Two Clowns", "Fortinbras", "Norwegian Captain", "English Ambassador", "Gertrude",
                  "Ophelia","Ghost of Hamlet's Father","Lord","Lady","Officer","Solider","Sailor","Messenger","Attendant"]

CHARACTERS_SHORT = ["King", "Ham", "Pol", "Hor", "Laer", "Volt", "Cor", "Ros", "Guil", "Osr", "Gent", "Priest",
                   "Mar","Ber","Fran","Rey","1 Play", "Clown", "Fort","Capt","Ambassador","Queen","Oph",
                   "Ghost","Lord","","","","Sailor","Mess","Servant"]

OTHER_BAD_WORDS = ["Enter", "Scene", "Exeunt", "Flourish", "Exit"]

FILE_NAME = "Hamlet.txt"


###
# Methods used to generate the correct response to a given line in the play
###
def removePunctuation(words):
    newWords = []
    for word in words:
        resultString = ""
        for char in word:
            if char not in string.punctuation:
                resultString += char
        newWords.append(resultString)
    return newWords

def indexMaxAndMinAllLines(fileName):
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
            words = removePunctuation(words)
            allLines.append(words)
    #print(lengths)
    maxLength = max(lengths)
    minLength = min(lengths)
    file.close()
    return allLines, firstWords, maxLength, minLength

def processHumanSpeech(speech, maxLength, minLength):
    processedSpeech = speech
    if len(speech) >= maxLength/2:
        processedSpeech = speech[-(minLength + 20):]
    if speech[-1:] == " ":
        processedSpeech = speech[0:len(speech) - 1]
    return processedSpeech

def respond(currentCharacter, previousLine, charactersShort):
    """ respond() is the main part of the algorithm for the robot's response.
    It returns a string with the lines following a part of a given previous line """
    allLines, firstWords, maxLength, minLength = indexMaxAndMinAllLines(FILE_NAME)
    respondString = ""
    charactersShort.remove(currentCharacter)
    for index1 in range(0, len(allLines)-1):
        currentLine = allLines[index1]
        currentLine = ' '.join(currentLine)
        if previousLine.lower() in currentLine.lower():
            prevLineNumber = index1
            for index2 in range(prevLineNumber + 1, len(allLines)):
                if firstWords[index2] not in charactersShort and firstWords[index2] not in OTHER_BAD_WORDS:
                    responseLine = allLines[index2]
                    responseLine = ' '.join(responseLine)
                    respondString = respondString + responseLine + "\n"
                elif firstWords[index2] in charactersShort:
                    break
    return respondString


def recognizeSpeech():
    """ Function that handles the transcription of audio into text via Google Speech API """
    # Reading in the Google API key
    with open("api-key-andy.json") as f:
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something!")
        audio = r.listen(source)

    humanInput = ""

    # Speech recognition using Google Speech Recognition
    try:
        humanInput = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        print("You said: " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    if len(humanInput) > 0:
        pass
    else:
        humanInput = "Try again"

    return humanInput

def postProcessHumanSpeech(speech):
    postProcessed = ""
    for char in speech:
        if char not in string.punctuation:
            postProcessed += char
    return postProcessed


allLines, firstWords, maxLength, minLength = indexMaxAndMinAllLines(FILE_NAME)

humanInput = recognizeSpeech()
print("Human input: ", humanInput)

processed = processHumanSpeech(humanInput, maxLength, minLength)
print("Processed: ", processed)

postProcessed = postProcessHumanSpeech(processed)
print("Post processed", postProcessed)

respondString = respond("Hor", postProcessed, CHARACTERS_SHORT)
print(respondString)