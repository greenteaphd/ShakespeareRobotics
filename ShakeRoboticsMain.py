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

def countLineNumbers(fileName):
    with open(fileName) as f:
        for i, l in enumerate(f):
            pass
        return i + 1

totalLineNumbers = countLineNumbers("Hamlet.txt")

def respond(inputText, character):
    if len(inputText) == 0:
        return "" #say nothing
    else:
        file = open("Hamlet.txt", "r")
        oneLine = file.readline()
        print (oneLine)

#respond("a", "character")

currentCharacter = "Fran."
previousLine = "Who's"
previousLine = "'Tis now"
charactersShort.remove(currentCharacter)
nonCharacters = ''.join(charactersShort)

lineNumber = 0
file = open("Hamlet.txt", "r")
prevLineNumber = 0

for currentLine in file:
    lineNumber += 1
    if previousLine in currentLine:
        prevLineNumber = lineNumber
    if (prevLineNumber != 0) and ((prevLineNumber + 1) == lineNumber) and (currentCharacter in currentLine):
        print(currentLine)
        prevLineNumber = lineNumber
        #break #comment in for 1 line response
    elif (prevLineNumber != 0) and ((prevLineNumber + 1) == lineNumber) and \
            ((currentCharacter in currentLine) or ("Enter" in currentLine)):
        break
    elif (prevLineNumber != 0) and ((prevLineNumber + 1) == lineNumber) and ((nonCharacters not in currentLine)):
        print(currentLine)
        prevLineNumber = lineNumber
        break



