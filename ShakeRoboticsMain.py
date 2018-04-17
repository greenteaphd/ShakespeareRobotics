# Andy Han, Joweina Hsiao, and Nikhil Smith
# COMP 380 - Robotics Project
# April 15th, 2018

###
# Static variables needed for respond() function
#   CHARACTERS_FULL is a list of all of the characters in Hamlet and their full names as listed in the Dramatis Personae
#   CHARACTERS_SHORT is a list of all of the characters in Hamlet and their shortened names as seen throughout the play's script
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

OTHER_BAD_WORDS = ["Enter", "Scene"]

FILE = open("Hamlet.txt", "r")


###
# Methods used to generate the correct response to a given line in the play
###

# indexAllLines is a helper function to respond(). It creates two lists: allLines and firstWords, which contains a list
# representation of either an entire line of the play, or simply the first word in a given line. These indexes do not
# match up with the ones in Hamlet.txt because it skips over blank lines.
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

# respond() is the main part of the algorithm for the robot's response. It returns a string with the lines following
# a part of a given previous line.
def respond(currentCharacter, previousLine, charactersShort):
    allLines, firstWords = indexAllLines(FILE)
    respondString = ""
    charactersShort.remove(currentCharacter)
    for index1 in range(0, len(allLines)-1):
        currentLine = allLines[index1]
        currentLine = ' '.join(currentLine)
        if previousLine in currentLine.lower():
            prevLineNumber = index1
            for index2 in range(prevLineNumber + 1, len(allLines)-1):
                if firstWords[index2] not in charactersShort and firstWords[index2] not in OTHER_BAD_WORDS:
                    responseLine = allLines[index2]
                    responseLine = ' '.join(responseLine)
                    respondString = respondString + responseLine + "\n"
                elif firstWords[index2] in charactersShort:
                    break
    return respondString


respondString = respond("Hor.", "is the question", CHARACTERS_SHORT)
print(respondString)