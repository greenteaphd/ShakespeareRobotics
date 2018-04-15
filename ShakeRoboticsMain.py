# Andy Han, Joweina Hsiao, and Nikhil Smith
# COMP 380 - Robotics Project
# April 8th, 2019


charactersFull = ["Claudius","Hamlet","Polonius","Horatio","Laertes","Voltemand","Cornelius","Rosencrantz",
                  "Guildenstern","Osric","Gentleman","Priest","Marcellus","Bernardo","Francisco","Reynaldo",
                  "Players", "Two Clowns", "Fortinbras", "Norwegian Captain", "English Ambassador", "Gertrude",
                  "Ophelia","Ghost of Hamlet's Father","Lord","Lady","Officer","Solider","Sailor","Messenger","Attendant"]

charactersShort = ["King","Ham.","Pol.","Hor.","Laer.","Volt.","Cor.","Ros.","Guil.","Osr.","Gent.","Priest.",
                   "Mar.","Ber.","Fran.","Rey.","1. Play.", "Clown.", "Fort.","Capt.","Ambassador.","Queen.","Oph.",
                   "Ghost.","Lord.","","","","Sailor.","Mess.","Servant."]

otherBadWords = ["Enter", "Scene"]

lineNumber = 0
file = open("Hamlet.txt", "r")
prevLineNumber = 0

def indexAllLines(file):
    allLines = []
    firstWords = []
    for currentLine in file:
        words = currentLine.split()
        if len(words) > 0:
            firstWord = words[0]
            firstWords.append(firstWord)
            allLines.append(words)
    return allLines, firstWords

allLines, firstWords = indexAllLines(file)

def respond(currentCharacter, previousLine, charactersShort):
    respondString = ""
    charactersShort.remove(currentCharacter)
    for index1 in range(0, len(allLines)-1):
        currentLine = allLines[index1]
        currentLine = ' '.join(currentLine)
        if previousLine in currentLine.lower():
            prevLineNumber = index1
            for index2 in range(prevLineNumber + 1, len(allLines)-1):
                if firstWords[index2] not in charactersShort and firstWords[index2] not in otherBadWords:
                    responseLine = allLines[index2]
                    responseLine = ' '.join(responseLine)
                    respondString = respondString + responseLine + "\n"
                elif firstWords[index2] in charactersShort:
                    break
    return respondString

respondString = respond("Hor.", "is the question", charactersShort)
print(respondString)

def getInputSpeech():
    import speech_recognition as sr

    with open("api-key.json") as f:
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
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
        humanInput
    else:
        humanInput = "Try again"
    return humanInput

#humanInput = getInputSpeech()
#print(humanInput)
#respondString = respond("Hor.", humanInput, charactersShort)
#print(respondString)