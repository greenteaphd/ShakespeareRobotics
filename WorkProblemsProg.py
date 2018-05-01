import string
import speech_recognition as sr

CHARACTERS_FULL = ["Nikhil", "Joweina", "Andy"]

CHARACTERS_SHORT = ["Nick", "Jo", "Andy"]

OTHER_BAD_WORDS = ["Enter", "Scene"]

FILE_NAME = "WorkProblems.txt"

def removePunctuation(inputString):
    """ Removes punctuation from a string """
    newString = inputString
    for char in inputString:
        if char not in string.punctuation:
            newString += char
    return newString

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

    human_input = ""

    # Speech recognition using Google Speech Recognition
    try:
        human_input = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        print("You said: " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    if len(human_input) > 0:
        pass
    else:
        human_input = "Try again"

    return human_input


maxLength, minLength = maxAndMinLines(FILE_NAME)
humanInput = recognizeSpeech()
processed = processHumanSpeech(humanInput, maxLength, minLength)
postProcessed = postProcessHumanSpeech(processed)
respondString = respond("Nick", postProcessed, CHARACTERS_SHORT)
print(respondString)
