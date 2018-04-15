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

def countLineNumbers(fileName):
    with open(fileName) as f:
        for i, l in enumerate(f):
            pass
        return i + 1

def respond(inputText, character):
    if len(inputText) == 0:
        return "" #say nothing
    else:
        file = open("Hamlet.txt", "r")
        oneLine = file.readline()
        print (oneLine)

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
    charactersShort.remove(currentCharacter)
    for index1 in range(0, len(allLines)-1):
        currentLine = allLines[index1]
        currentLine = ' '.join(currentLine)
        if previousLine in currentLine:
            prevLineNumber = index1
            for index2 in range(prevLineNumber + 1, len(allLines)-1):
                if firstWords[index2] not in charactersShort and firstWords[index2] not in otherBadWords:
                    responseLine = allLines[index2]
                    responseLine = ' '.join(responseLine)
                    print(responseLine)
                elif firstWords[index2] in charactersShort:
                    break

respond("Hor.","That was and", charactersShort)